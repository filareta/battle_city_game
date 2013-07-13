from collections import deque

from settings import SIZE_X, SIZE_Y, TILE_SIZE, MAPS, CONTENT
from vector import Vec2D
from player import Player
from enemy import Enemy
from static_objects import Wall

import math


class Tile:
    def __init__(self, x, y, content):
        self.position = Vec2D(x, y)
        self.content = content
        self._set_content(content)

    def _set_content(self, content):
        self.content = CONTENT[content]

    def empty(self):
        return self.content == '0'

    def passable(self):
        return self.content != 'B' and self.content != 'W' and self.content != 'F'

    def is_brick(self):
        return self.content == 'B'

    def is_wall(self):
        return self.content == 'W'

    def __str__(self):
        return self.content


class World:
    players = {'1': None, '2': None}
    enemies = []
    walls = []
    bounds = []
    phoenix = []
    multiplayer = False

    def __init__(self, map_file, multiplayer):
        self.multiplayer = multiplayer
        self.world = [[None for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self.aim_tiles = [[0 for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self.pathing = [[None for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self._read_map(map_file)

    def _read_map(self, map_file):
        with open(map_file) as file_map:
            for i, line in enumerate(file_map):
                for j, item in enumerate(item for item in line if item != ' ' and item != '\n'):
                    if item != ' ' and item != '\n':
                        self._extend_map(i, j, item)

        # self.print_world()

    def print_world(self):
        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                print(self.world[x][y], end=" ")

            print()

    def print_aim_lines(self):
        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                print(self.aim_tiles[x][y], end=" ")

            print()

    def _create_object(self, item, position):
        if item == 'Y':
            self.players['1'] = Player(position, 1)
        elif item == 'G' and self.multiplayer:
            self.players['2'] = Player(position, 2)
        elif item == 'F':
            self.phoenix.append(position)
        elif item == 'E':
            new_enemy = Enemy(position)
            self.enemies.append(Enemy(position))
            if (len(self.enemies) + 1) % 3 == 0:
                new_enemy.target = "phoenix"
        elif item == 'B':
            self.walls.append(Wall(position, breakable=True))
        elif item == 'W':
            self.walls.append(Wall(position, breakable=False))
        elif item == '#':
            self.bounds = position

    def _extend_map(self, i, j, item):

        if item != '#' and item != 'Y' and item != 'G' and item != 'E':
            self.world[j][i] = Tile(j, i, item)

        elif j == 0 or j == SIZE_X - 1 or i == 0 or i == SIZE_Y - 1:
            self.world[j][i] = Tile(j, i, item)

        else:
            self.world[j][i] = Tile(j, i, '0')

        self._create_object(item, Vec2D(j, i))

    def set_content(self, item, coords):
        for tile in coords:
            self.world[tile[0]][tile[1]].content = item

    def in_range(self, x, y):
        return x >= 0 and x < SIZE_X and y >= 0 and y < SIZE_Y

    def get_next_direction(self, from_pos):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                self.pathing[x][y] = None

        found_cell = None
        from_pos.x = math.floor(from_pos.x)
        from_pos.y = math.floor(from_pos.y)
        from_cell = self.get_block_coords(from_pos.x, from_pos.y)

        if self.aim_tiles[from_cell.x][from_cell.y] != 0:
            direction = (from_cell * TILE_SIZE) - from_pos

            return (direction, self.aim_tiles[from_cell.x][from_cell.y])

        queue = deque()
        queue.append(from_cell)

        while queue and found_cell is None:
            cell = queue.popleft()
            neighbours = self.passable_neighbours(cell)
            for n in neighbours:
                if self.pathing[n.x][n.y] is not None:
                    continue

                queue.append(n)
                self.pathing[n.x][n.y] = cell

                if self.aim_tiles[n.x][n.y] != 0:
                    found_cell = n
                    break

        if found_cell is not None:
            cell = found_cell
            while self.pathing[cell.x][cell.y] != from_cell:
                cell = self.pathing[cell.x][cell.y]

            direction = (cell * TILE_SIZE) - from_pos

            one_way = Vec2D(direction.x, direction.y)
            one_way.x = 0
            one_way.y = 0

            if direction.y != 0:
                one_way.y = TILE_SIZE if direction.y > 0 else -TILE_SIZE

            new_dir = self.validify_direction(from_pos, one_way)

            if not new_dir.zero():
                return (new_dir, self.aim_tiles[cell.x][cell.y])
            else:
                one_way = Vec2D(direction.x, direction.y)
                one_way.x = 0
                one_way.y = 0

                if direction.x != 0:
                    one_way.x = TILE_SIZE if direction.x > 0 else -TILE_SIZE

                new_dir = self.validify_direction(from_pos, one_way)

                return (new_dir, self.aim_tiles[cell.x][cell.y])
        else:
            return (Vec2D(0, 0), '1')

    def passable_neighbours(self, cell):
        dirs = [Vec2D(1, 0), Vec2D(0, -1), Vec2D(-1, 0), Vec2D(0, 1)]
        cells = [direction + cell for direction in dirs]
        return filter((lambda c: self.in_range(c.x, c.y) and self[c.x][c.y].passable()), cells)

    def kill(self):
        for i, enemy in enumerate(self.enemies):
            if not enemy.alive:
                self.clear_content(enemy.coords[0], 'E')
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        if self.players['1'].dead:
            self.clear_content(self.players['1'].coords[0], 'Y')
        if self.multiplayer and self.players['2'].dead:
            self.clear_content(self.players['2'].coords[0], 'G')

    def __getitem__(self, index):
        return self.world[index]

    def get_all_block_coords(self, pixels_x, pixels_y):
        blocks = []

        blocks.append(self.get_block_coords(pixels_x, pixels_y))
        if pixels_x % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x + TILE_SIZE, pixels_y))

        if pixels_y % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x, pixels_y + TILE_SIZE))

        if pixels_x % TILE_SIZE != 0 and pixels_y % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x + TILE_SIZE, pixels_y + TILE_SIZE))

        return blocks

    def get_block_coords(self, pixels_x, pixels_y):
        return Vec2D(math.floor(math.floor(pixels_x) / TILE_SIZE), math.floor(math.floor(pixels_y) / TILE_SIZE))

    def get_center_block(self, top_left_x, top_left_y):
        return self.get_block_coords(top_left_x + TILE_SIZE / 2, top_left_y + TILE_SIZE / 2)

    def valid_position(self, position):
        blocks = self.get_all_block_coords(position.x, position.y)

        for tile in blocks:
            if not self.in_range(tile.x, tile.y) or not self[tile.x][tile.y].passable():
                return False

        return True

    def enemy_hit(self, position, except_for=None):
        for enemy in self.enemy_sprites:
            if enemy != except_for and enemy.has_hit(position):
                return enemy

        return None

    def enemy_hit_tile(self, position, except_for=None):
        corners = [
            Vec2D(position.x + 1, position.y + 1),
            Vec2D(position.x + TILE_SIZE - 1, position.y + 1),
            Vec2D(position.x + 1, position.y + TILE_SIZE - 1),
            Vec2D(position.x + TILE_SIZE - 1, position.y + TILE_SIZE - 1),
        ]

        for corner in corners:
            enemy = self.enemy_hit(corner, except_for=except_for)
            if enemy is not None:
                return enemy

        return None

    def player_hit(self, position):
        for player in self.player_sprites.values():
            if player and player.has_hit(position):
                return player

        return None

    def player_hit_tile(self, position):
        corners = [
            Vec2D(position.x + 1, position.y + 1),
            Vec2D(position.x + TILE_SIZE - 1, position.y + 1),
            Vec2D(position.x + 1, position.y + TILE_SIZE - 1),
            Vec2D(position.x + TILE_SIZE - 1, position.y + TILE_SIZE - 1),
        ]

        for corner in corners:
            player = self.player_hit(corner)
            if player is not None:
                return player

        return None

    def _tile_size_if_0(self, value):
        return value if value > 0 else TILE_SIZE

    def validify_direction(self, current_position, direction):
        """ Works only when direction is not diagonal """
        newpos = current_position + direction

        if direction.zero():
            return direction

        if self.valid_position(newpos):
            return direction

        if direction.x > 0:
            next_block = self.get_block_coords(current_position.x + direction.x + TILE_SIZE, current_position.y)
            direction.x = TILE_SIZE - self._tile_size_if_0(current_position.x % TILE_SIZE)
        elif direction.x < 0:
            next_block = self.get_block_coords(current_position.x + direction.x, current_position.y)
            direction.x = -(current_position.x % TILE_SIZE)
        elif direction.y > 0:
            next_block = self.get_block_coords(current_position.x, current_position.y + direction.y + TILE_SIZE)
            direction.y = TILE_SIZE - self._tile_size_if_0(current_position.y % TILE_SIZE)
        elif direction.y < 0:
            next_block = self.get_block_coords(current_position.x, current_position.y + direction.y)
            direction.y = -(current_position.y % TILE_SIZE)

        return direction

    def update_aim_lines(self):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                self.aim_tiles[x][y] = 0

        for player_num, player in self.players.items():
            if player and not player.dead:
                tile = self.get_center_block(player.coords.x, player.coords.y)

                directions = [
                    Vec2D(-1, 0),
                    Vec2D(1, 0),
                    Vec2D(0, 1),
                    Vec2D(0, -1),
                ]

                for direction in directions:
                    pos = tile + direction

                    while self.in_range(pos.x, pos.y) and self[pos.x][pos.y].passable():
                        self.aim_tiles[pos.x][pos.y] = player_num
                        pos = pos + direction

        # self.print_aim_lines()

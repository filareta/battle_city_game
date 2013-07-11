def rect_collision(rect1, rect2):
    w = 0.5 * (rect1.width + rect2.width)
    h = 0.5 * (rect1.height + rect2.height)
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    if abs(dx) <= w and abs(dy) <= h:
        wy = w * dy
        hx = h * dx
        if wy > hx and wy > - hx:
            return "top"
        elif wy > hx and wy <= -hx:
            return "left"
        elif wy <= hx and wy > -hx:
            return "right"
        elif wy <= hx and wy <= -hx:
            return "bottom"

def reactor(rect, side):
    if side == "top":
        rect.top += 10
    if side == "bottom":
        rect.bottom -= 10
    if side == "left":
        rect.left += 10
    if side == "right":
        rect.right -= 10


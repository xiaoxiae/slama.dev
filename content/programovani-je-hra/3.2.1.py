x = 100
y = 120
dx = 3
dy = 5
r = 30


def setup():
    size(400, 400)


def draw():
    global x, y, dx, dy, r

    background(255)
    ellipse(x, y, r * 2, r * 2)

    if x >= width - r:
        dx = -dx

    if x <= r:
        dx = -dx

    if y >= height - r:
        dy = -dy

    if y <= r:
        dy = -dy

    x = x + dx
    y = y + dy

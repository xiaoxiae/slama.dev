def sierpinski(n, x1, y1, x2, y2, x3, y3):
    if n == 0:  # base case
        return

    xa = (x1 + x2) / 2
    ya = (y1 + y2) / 2
    xb = (x1 + x3) / 2
    yb = (y1 + y3) / 2
    xc = (x2 + x3) / 2
    yc = (y2 + y3) / 2

    sierpinski(n - 1, x1, y1, xa, ya, xb, yb)
    sierpinski(n - 1, x2, y2, xa, ya, xc, yc)
    sierpinski(n - 1, x3, y3, xb, yb, xc, yc)

    fill(255)
    triangle(xa, ya, xb, yb, xc, yc)


def setup():
    size(400, 400)
    background(255)


def draw():
    x1 = width / 2
    y1 = 0
    x2 = 0
    y2 = height
    x3 = width
    y3 = height

    fill(0)
    triangle(x1, y1, x2, y2, x3, y3)
    sierpinski(6, x1, y1, x2, y2, x3, y3)

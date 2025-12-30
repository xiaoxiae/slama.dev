x = 0
y = 0


def setup():
    size(400, 400)


def draw():
    global x, y

    background(255)

    rect(x, y, 30, 30)


def keyPressed():
    global x, y

    if key == "w":
        y -= 10
    if key == "a":
        x -= 10
    if key == "s":
        y += 10
    if key == "d":
        x += 10

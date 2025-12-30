x = 0
y = 0

# pokud jsou dané klávesy aktuálně zmáčknuté
#          w      a      s      d
pressed = [False, False, False, False]

# rychlost v daném směru
velocity = [0, 0, 0, 0]


def setup():
    size(400, 400)


def draw():
    global x, y, pressed

    i = 0
    while i < 4:
        # float() je tu proto, že / v Processingu dělí celočíselně
        if pressed[i]:
            velocity[i] += float(1 - velocity[i]) / 5
        else:
            velocity[i] += float(-velocity[i]) / 5

        i += 1

    # přičítáme rychlosti doleva/doprava a nahoru/dolů
    y += (velocity[2] - velocity[0]) * 5
    x += (velocity[3] - velocity[1]) * 5

    background(255)

    rect(x, y, 30, 30)


def keyPressed():
    global pressed

    if key == "w":
        pressed[0] = True
    if key == "a":
        pressed[1] = True
    if key == "s":
        pressed[2] = True
    if key == "d":
        pressed[3] = True


def keyReleased():
    global pressed

    if key == "w":
        pressed[0] = False
    if key == "a":
        pressed[1] = False
    if key == "s":
        pressed[2] = False
    if key == "d":
        pressed[3] = False

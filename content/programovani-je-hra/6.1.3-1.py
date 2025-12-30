ptaci = []


class Ptak:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def posun(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.dx *= -1

        if self.y < 0:
            self.dy *= -1

        if self.y > height:
            self.dy *= -1

        if self.x > width:
            self.dx *= -1

    def vykresli(self):
        ellipse(self.x, self.y, 10, 10)


def setup():
    size(400, 400)


def draw():
    background(255)

    i = 0
    while i < len(ptaci):
        ptak = ptaci[i]

        ptak.posun()
        ptak.vykresli()

        i += 1


def mousePressed():
    global ptaci

    ptak = Ptak(mouseX, mouseY, 3, 3)
    ptaci.append(ptak)

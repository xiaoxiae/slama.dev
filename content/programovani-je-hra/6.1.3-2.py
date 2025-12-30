ptaci = []
rozhled = 100


def pythagoras(x1, x2, y1, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Ptak:
    def __init__(self, x, y, dx, dy):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(dx)
        self.dy = float(dy)

    def posun(self):
        alignment = self.spocitej_alignment()

        self.dx = alignment[0]
        self.dy = alignment[1]

        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.dx *= -1
            self.x = 0

        if self.y < 0:
            self.dy *= -1
            self.y = 0

        if self.y > height:
            self.dy *= -1
            self.y = height

        if self.x > width:
            self.dx *= -1
            self.x = width

    def vykresli(self):
        # TODO: trojúhelníky
        ellipse(self.x, self.y, 10, 10)

    def spocitej_alignment(self):
        global ptaci, rozhled

        ndx = 0
        ndy = 0

        i = 0
        while i < len(ptaci):
            ptak = ptaci[i]

            # vzdálenost toho našeho od dalšího
            c = pythagoras(self.x, ptak.x, self.y, ptak.y)

            if c < rozhled:
                ndx += ptak.dx
                ndy += ptak.dy

            i += 1

        ndx /= len(ptaci)
        ndy /= len(ptaci)

        # magie
        norma = (ndx**2 + ndy**2) ** (1 / 2.0)
        if norma != 0:
            ndx /= norma
            ndy /= norma

        return [ndx, ndy]


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

    # vykreslení počtu ptáků
    textAlign(LEFT, TOP)
    fill(0)
    textSize(32)
    text(len(ptaci), 10, 10)


def mousePressed():
    global ptaci

    ptak = Ptak(mouseX, mouseY, 3, 3)
    ptaci.append(ptak)

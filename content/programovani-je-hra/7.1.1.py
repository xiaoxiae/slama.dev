import random


class Flappy:
    def __init__(self, x, y, r, dx, dy, gravitace, velikost_skoku):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.r = r
        self.gravitace = gravitace
        self.velikost_skoku = velikost_skoku

    def vykresli(self):
        ellipse(self.x, self.y, self.r, self.r)

    def pohni_se(self):
        self.x += self.dx
        self.y += self.dy
        self.dy -= self.gravitace

        if self.y < 0:
            self.y = height

        if self.y > height:
            self.y = 0

    def skoc(self):
        self.dy = self.velikost_skoku


class Prekazka:
    def __init__(self, x, w, h, m):
        self.x = x
        self.w = w
        self.h = h
        self.m = m

    def vykresli(self):
        # kus nahoře
        rect(self.x, 0, self.w, self.h)

        # kus dole
        rect(self.x, self.h + self.m, self.w, height - self.h - self.m)

    def kolize(self, flappy):
        pass


def keyPressed():
    global flappy

    if key == " ":
        flappy.skoc()


def mousePressed():
    global flappy

    if mouseButton == LEFT:
        flappy.skoc()

    # TODO: na kolečko myši


flappy = Flappy(100, 100, 15, 2, 0, -0.2, -4)
prekazky = []


def setup():
    global prekazky

    size(400, 400)

    pocet_prekazek = 30
    vzdalenost_prekazek = 200
    sirka_prekazek = 30

    mezera_prekazek = 80  # TODO zmenšování

    for i in range(pocet_prekazek):
        x = (i + 1) * vzdalenost_prekazek
        h = random.randint(50, 250)

        prekazky.append(Prekazka(x, sirka_prekazek, h, mezera_prekazek - i / 2.0))


def draw():
    global flappy, prekazky

    translate(-flappy.x + width / 2, 0)

    background(255)
    flappy.vykresli()
    flappy.pohni_se()

    for i in range(len(prekazky)):
        prekazky[i].vykresli()

    # lepší grafika
    # - barvy
    # - pozadí
    # - otáčení flappy birda, když padá => lepší flappy bird!

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

        self.umrel = False

    def vykresli(self):
        x = self.x + 15
        y = self.y + self.dy * 3

        d = sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        nx = (self.x - x) / d
        ny = (self.y - y) / d

        fill(180, 0, 0)
        triangle(
            self.x,
            self.y + 5,
            self.x,
            self.y - 5,
            self.x + nx * (-15),
            self.y + ny * (-15),
        )

        fill(255, 160, 0)
        ellipse(self.x, self.y, self.r, self.r)

    def pohni_se(self):
        self.x += self.dx
        self.y += self.dy
        self.dy -= self.gravitace

        if self.y < 0:
            if self.gravitace < 0:
                self.y = 0
            else:
                exit()

        if self.y > height:
            if self.gravitace < 0:
                exit()
            else:
                self.y = height

    def skoc(self):
        if not self.umrel:
            self.dy = self.velikost_skoku

    def umri(self):
        if not self.umrel:
            self.dx = 0
            self.dy = 0
            self.umrel = True

    def prohod(self):
        self.velikost_skoku = -self.velikost_skoku
        self.gravitace = -self.gravitace


class Prekazka:
    def __init__(self, x, w, h, m, prohazujici):
        self.x = x
        self.w = w
        self.h = h
        self.m = m
        self.prohazujici = prohazujici

    def vykresli(self):
        if self.prohazujici:
            fill(0, 100, 0)
        else:
            fill(0, 200, 0)

        rect(self.x, 0, self.w, self.h)

        rect(self.x, self.h + self.m, self.w, height - self.h - self.m)

    def kolize_ctverec(self, flappy, x, y, w, h):
        x = abs(flappy.x - (x + w / 2))
        y = abs(flappy.y - (y + h / 2))
        r = flappy.r / 2

        dx, dy = x - w / 2, y - h / 2

        return (
            not (x > w / 2 + r or y > h / 2 + r)
            and (x < w / 2 or y < h / 2)
            or sqrt(dx**2 + dy**2) < r
        )

    def kolize(self, flappy):
        rectangles = [
            [self.x, 0, self.w, self.h],
            [self.x, self.h + self.m, self.w, height - self.h - self.m],
        ]

        return self.kolize_ctverec(flappy, *rectangles[0]) or self.kolize_ctverec(
            flappy, *rectangles[1]
        )


def keyPressed():
    global flappy

    if key == " ":
        flappy.skoc()


def mousePressed():
    global flappy

    if mouseButton == LEFT:
        flappy.skoc()


flappy = Flappy(100, 100, 15, 2, 0, -0.2, -4)
prekazky = []

vzdalenost_prekazek = 200

skore = 0


def setup():
    global prekazky, vzdalenost_prekazek

    size(400, 400)

    pocet_prekazek = 45
    sirka_prekazek = 30

    mezera_prekazek = 80

    for i in range(pocet_prekazek):
        x = (i + 1) * vzdalenost_prekazek
        h = random.randint(50, 250)

        prohazujici = False
        if random.random() < (1 / 10.0):
            prohazujici = True

        if prohazujici:
            mezera_prekazek *= 2

        prekazky.append(
            Prekazka(x, sirka_prekazek, h, mezera_prekazek - i / 2.0, prohazujici)
        )

        if prohazujici:
            mezera_prekazek /= 2


def draw():
    global flappy, prekazky, skore

    translate(-flappy.x + width / 2, 0)

    background(
        flappy.y / height * 173,
        flappy.y / height * 216,
        139 + flappy.y / height * (230 - 139),
    )

    flappy.vykresli()
    flappy.pohni_se()

    for i in range(len(prekazky)):
        if prekazky[i].kolize(flappy):
            flappy.umri()

        prekazky[i].vykresli()

    nove_skore = flappy.x // vzdalenost_prekazek

    if skore != nove_skore:
        if prekazky[skore].prohazujici:
            flappy.prohod()

        skore = nove_skore

    fill(0)
    textSize(32)
    textAlign(CENTER, CENTER)
    text(nove_skore, flappy.x, 25)

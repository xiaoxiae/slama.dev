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

    def kolize_ctverec(self, flappy, x, y, w, h):
        """Vrátí True, pokud flappy koliduje se čtvercem určeným bodem (x, y) a jeho šířkou/výškou."""
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
        # čtverce, které testujeme
        rectangles = [
            [self.x, 0, self.w, self.h],
            [self.x, self.h + self.m, self.w, height - self.h - self.m],
        ]

        # otestuje, zda flappy koliduje z jedním ze čtverců
        # * je magie, která "rozbalí" pole do volání funkce
        # self(*pole) je to samé jako self(pole[0], pole[1],...)
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
        if prekazky[i].kolize(flappy):
            fill(0)
        else:
            fill(255)

        prekazky[i].vykresli()

    # lepší grafika
    # - barvy
    # - pozadí
    # - otáčení flappy birda, když padá => lepší flappy bird!

    # upgrady
    # - náhodné prohození gravitace
    # - zrychlování

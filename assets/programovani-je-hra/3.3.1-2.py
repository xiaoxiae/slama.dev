stupne = 0
smer = 3

def setup():  # kód, který se vykoná pouze jednou
    size(400, 400)   # nastavení velikosti okna

def draw():  # kód, který se dokola opakuje
    global stupne, smer
    
    background(255)  # nastavení pozadí na bílou
    line(200, 100, 200, 230)
    line(200, 230, 220, 300)
    line(200, 230, 180, 300)
    line(200, 150, 180, 200)
    ellipse(200, 100, 50, 50)
    rect(-1, 300, 401, 401)
    
    stupne = stupne - smer
    
    if stupne > 100:
        smer = -smer
    
    if stupne < 0:
        smer = -smer
    
    translate(200, 150)
    rotate(radians(-stupne))
    line(0, 0, 20, 50)

stupne = 0

def setup():  # kód, který se vykoná pouze jednou
    size(400, 400)   # nastavení velikosti okna

def draw():  # kód, který se dokola opakuje
    global stupne

    translate(width / 2, height / 2)
    rotate(radians(-stupne))
    translate(-width / 2, -height / 2)
    
    background(255)  # nastavení pozadí na bílou
    line(200, 100, 200, 230)
    line(200, 230, 220, 300)
    line(200, 230, 180, 300)
    line(200, 150, 180, 200)
    line(200, 150, 220, 200)
    ellipse(200, 100, 50, 50)
    rect(-200, 300, 901, 401)
    
    stupne += 5


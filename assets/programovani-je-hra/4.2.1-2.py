x = 0
y = 0

def setup():
    size(400, 400)

def draw():
    global x, y
    
    background(255)
    
    ellipse(x, y, 30, 30)
    
    x += (mouseX - x) / 10
    y += (mouseY - y) / 10
    

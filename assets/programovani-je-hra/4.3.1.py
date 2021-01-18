def setup():
    size(400, 400)
    
    x = 0
    y = 0
    while (y <= 400):
        if ((x + y) % 100 == 0):
            fill(0)
        else:
            fill(255)
            
        rect(x, y, 50, 50)
        
        x += 50
        if (x >= 400):
            x = 0
            y += 50

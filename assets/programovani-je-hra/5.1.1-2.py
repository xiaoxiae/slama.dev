sirka = 20
vyska = sirka

stav = [[0] * sirka for _ in range(vyska)]
vek  = [[1000] * sirka for _ in range(vyska)]

# GLOBAL PROMENNE ^

def setup():
    global stav
    
    size(800, 800)
    background(255)

def draw():
    global stav, sirka, vyska
    
    y = 0
    while y < vyska:
        x = 0
        
        while x < sirka:
            if stav[x][y] == 0:
                fill(vek[x][y] * 10)
            else:
                fill(125 + vek[x][y] * 10, 0, 125 + vek[x][y] * 10)
            
            rozmer = width // sirka
            rect(x * rozmer, y * rozmer, rozmer, rozmer)
            
            x += 1
            
        y += 1


def update_state():
    # 1. Any live cell with two or three live neighbours survives.
    # 2. Any dead cell with three live neighbours becomes a live cell.
    # 3. All other cells die in the next generation.
    global stav, vek
    
    novy_stav = [[0] * sirka for _ in range(vyska)]
    
    y = 0
    while y < vyska:
        x = 0
        
        while x < sirka:
            if stav[x][y] == 1:
                if pocet_sousedu(x, y) == 2 or pocet_sousedu(x, y) == 3:
                    novy_stav[x][y] = 1
                    vek[x][y] += 1
                else:
                    novy_stav[x][y] = 0
                    vek[x][y] = 0
            else:
                if pocet_sousedu(x, y) == 3:
                    novy_stav[x][y] = 1
                    vek[x][y] = 0
                else:
                    novy_stav[x][y] = 0
                    vek[x][y] += 1
                                            
            x += 1
            
        y += 1
        
    stav = novy_stav
    

def pocet_sousedu(x, y):
    global stav, vyska, sirka

    pocet = 0
    
    smer = [[1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
            [1, 1],
            [-1, 1],
            [1, -1],
            [-1, -1]]
    
    i = 0
    while i < len(smer):
        new_x = x + smer[i][0]
        new_y = y + smer[i][1]
    
        if new_x >= 0 and new_y >= 0 and new_x < sirka and new_y < vyska:
            if stav[new_x][new_y] == 1:
                pocet += 1
        
        i += 1
    
    return pocet


def keyPressed():
    if key == ' ':
        update_state()

def mousePressed():
    global stav
    
    if mouseButton == LEFT:
        rozmer = width // sirka
        
        x = mouseX // rozmer
        y = mouseY // rozmer
 
        if stav[x][y] == 1:
            stav[x][y] = 0
        else:
            stav[x][y] = 1
        vek[x][y] = 0


---
language: cz
title: Programování je Hra
hidden: true
---

- .
{:toc}

Vítejte na stránce kurzu Programování je Hra!

Kurz bude vyučovaný online formou, každý čtvrtek od **15:30** do **17:00** na stránce **[https://meet.jit.si/programovani-je-hra](https://meet.jit.si/programovani-je-hra)**. Cílem je se seznámit se základy programování v jazyce Python.

### Kontakt
Pokud byste se chtěli na cokoliv zeptat, tak jsem k zastižení tady:

- **Email:** `tomas [zavináč] slama [tečka] dev`
- **Discord:** `Tomáš Sláma#6609`

### Příklady
Příklady jsou **nepovinné**, nejsme ve škole. Jsou tu hlavně pro to, abyste se lépe pochopili probíranou látku a rozhodně se nebudu zlobit, když za kurz nesplníte všechny. Na druhou stranu budu rád, když se alespoň část pokusíte vyřešit 🙂. Těžké příklady jsou označené hvězdičkou (⭐).

### 1. hodina (10. 12. 2020)

#### Proměnné
- "krabičky" se jmény, které si drží informace

```python
a = 123               # krabička a, která drží číslo 123
b = "Tohle je věta."  # krabička b, která drží větu
c = a                 # krabička c, která si uloží, co je v a

# print(...) vypíše cokoliv, co do něho dáte
# pro nás zatím magie
print(a)
print(b)
print(c)
```

- jméno krabičky může obsahovat:
	- velká a malá písmena
	- čísla (ale ne jako první znak!)
	- symbol `_`

```python
123 = 1   # neplatné, jméno nesmí začínat číslem
a+b = 123 # neplatné, jméno nesmí obsahovat +
```

1. Máte číselné proměnné `a` a `b`. Napište program, který prohodí jejich obsah. [[řešení](/assets/programovani-je-hra/1.1.1.py)]
	* Zvládnete to bez použití pomocné proměnné (a bez použití `a, b = b, a`)? ⭐ [[řešení](/assets/programovani-je-hra/1.1.1-1.py)]

#### Aritmetika

{:.rightFloatBox}
<div markdown="1">
**Zajímavost:** místo `a = a + 3` můžeme používat `a += 3` (funguje i pro ostatní operátory). Zápis je tak stručnější a přehlednější.
</div>

- s proměnnými toho příliš nezvládneme, umět počítat
- Python umí vyhodnocovat aritmetické výrazy
	- běžné jsou `+`, `-`, `*`, `/`
	- umí používat také závorky `(`, `)`
	- další operátory:
		- `//` -- celočíselné dělení
		- `%` -- zbytek po dělení
		- `**` -- mocnění

```python
a = 12 + 6 - 5   # a = 13
b = a / 2        # b = 6.5
c = -b           # c = -6.5
d = 2 + 2 * 2    # d = 6
e = (2 + 2) * 2  # e = 8
f = 2 ** 3       # f = 8

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
```

1. Máte proměnnou `a`, která udává délku strany kostky. Vypište její obsah. [[řešení](/assets/programovani-je-hra/1.2.1.py)]
	* Vypište její plochu. [[řešení](/assets/programovani-je-hra/1.2.1-1.py)]
	* Vypište plochu největší koule, která se do kostky vejde. [[řešení](/assets/programovani-je-hra/1.2.1-2.py)]
	* Vypište plochu největší koule, do které se kostka vejde. ⭐ [[řešení](/assets/programovani-je-hra/1.2.1-3.py)]
2. Máte proměnnou `celsius` s číselnou hodnotou. Vypište, kolik je to Fahrenheitů ([odkaz na Wiki](https://cs.wikipedia.org/wiki/Stupeň_Fahrenheita), pokud nevíte, jak převod vypadá). [[řešení](/assets/programovani-je-hra/1.2.2.py)]

#### `if`, `else`

{:.rightFloatBox}
<div markdown="1">
**Zajímavost:** existuje také `elif`, které je možné zapojit za `if`, které se zkusí vykonat jen pokud se `if` nevykoná.
</div>

- vykonávání kódu, pokud něco platí/neplatí
- pokud je podmínka pravdivá, tak se vykonají **všechny následující** (správně) **odsazené řádky**
- `else` je nepovinné, ale může se hodit

```python
a = 10

if a == 10:
	print("a je 10!")           # vykoná se

if a < 3:
	print("a je menší než 3!")  # nevykoná se
else:
	print("a je větší nebo rovno 3!")  # vykoná se
```

- `if`y můžeme **vnořovat** do sebe a vytvářet tak komplexnější podmínky

```python
a = 10

if a < 100:
	if a < 50:
		print("a je menší než 50")
	else:
		print("a je mezi 50 a 100")
else:
	print("a je větší nebo rovno 100")
```

1. Máte číselné proměnné `a` a `b`. Vypište `<`, `>` nebo `=` podle toho, zda je `a` menší/větší/rovné. [[řešení](/assets/programovani-je-hra/1.3.1.py)]
2. Máte číselnou proměnnou `a`. Napište program, který vypíše `Sudé!` když je `a` sudé a `Liché!`, když je `a` liché. Použijte operátor `%` (zbytek po dělení). [[řešení](/assets/programovani-je-hra/1.3.2.py)]
	- Zvládnete to i bez operátoru `%`? [[řešení](/assets/programovani-je-hra/1.3.2-1.py)]
3. Máte číselné proměnné `a`, `b` a `c`, které mají různé hodnoty. Vypište tato čísla od nejmenšího po největší. Využijte toho, že `if`y mohou být vnořené. ⭐ [[řešení](/assets/programovani-je-hra/1.3.3.py)]

### 2. hodina (17. 12. 2020)

#### Uživatelský vstup
- čtení věcí, které uživatelé zadají

```py
veta  = input()       # čtení věty
cislo = int(input())  # čtení čísla

print(veta)
print(cislo)
```

1. Chceme se uživatele zeptat, kolik mu je let. Vypište jeho věk a pokud mu je více než 20, napište `Je ti více než 20!`. [[řešení](/assets/programovani-je-hra/2.1.1.py)]

#### Smyčky
- opakování části kódu, dokud něco platí

```py
i = 0

# vypíše čísla od 0 do 9
while i < 10:
	print(i)
	i = i + 1
```

- smyčky také můžeme vnořovat do sebe

```py
i = 0

# vypíše dvojice čísel od 0 do 9
while i < 10:
	j = 0
	
	while j < 10:
		print(i, j)  # vypsání dvou věcí
		j = j + 1

	i = i + 1
```

1. Máte číselnou proměnnou `a`. Vypište všechna čísla od {% latex %}1{% endlatex %} do `a`. [[řešení](/assets/programovani-je-hra/2.2.1.py)]
	* Vypište jen sudá čísla. [[řešení](/assets/programovani-je-hra/2.2.1-1.py)]
2. Máte číselnou proměnnou `a`. Vypište všechna čísla, která dělí `a`. [[řešení](/assets/programovani-je-hra/2.2.2.py)]
	* Vypište její prvočíselný rozklad. ⭐ [[řešení](/assets/programovani-je-hra/2.2.2-1.py)]
3. Chceme napsat robota, který bude hádat čísla od {% latex %}1{% endlatex %} do {% latex %}100{% endlatex %}. Uživateli řekne číslo, které hádá, a zeptá se ho, zda je uživatelovo menší, nebo větší. ⭐ [[řešení](/assets/programovani-je-hra/2.2.3.py)]

#### Pole
- hodně proměnných za sebou

```py
x = [0, 0, 0]

x[0] = 1
x[1] = 10
x[2] = 3

print(x[0])    # vypíše hodnotu na první pozici
print(x[1])    # vypíše hodnotu na druhé pozici
print(x[2])    # vypíše hodnotu na třetí pozici

print(x)       # vypíše pole: [1, 10, 3]
print(len(x))  # vypíše délku pole (3)
```

1. Máte pole čísel `pole`. Vypište:
	- počet čísel v poli. [[řešení](/assets/programovani-je-hra/2.3.1-1.py)]
	- největší číslo v poli. [[řešení](/assets/programovani-je-hra/2.3.1-2.py)]
	- nejmenší číslo v poli. [[řešení](/assets/programovani-je-hra/2.3.1-3.py)]
	- součet čísel v poli. [[řešení](/assets/programovani-je-hra/2.3.1-4.py)]

- pole jdou také „rozšiřovat“ pomocí funkcí:
	- `pole.append(prvek)` přidá na konec pole prvek
	- `pole.pop()` odebere z konce pole poslední prvek a vrátí ho

### 3. hodina (7. 1. 2021)

#### Processing
- „sketchbook“ -- nástroj na tvorbu animací, her, vizualizací
- programování v JavaScriptu, Javě a Pythonu

##### Instalace
1. stáhni a nainstaluj následující soubor: [https://download.processing.org/processing-3.5.4-windows64.zip](https://download.processing.org/processing-3.5.4-windows64.zip)
2. po otevření aplikace `Processing 3` v pravém horním rohu rozklikni, vyber `Add Mode...`
3. nainstaluj z nabídky Python mód
4. restartuj a Python mód vyber

##### Odbočka: funkce
- „krabička“, která vezme nějaké hodnoty, vykoná kus kódu poté něco vrátí

```py
def funkce(x):    # bere nějakou hodnotu
	y = x + 1
	return y      # a vrátí ji o 1 zvětšenou

print(funkce(4))  # vypíše 5
print(funkce(-3)) # vypíše -2
```

- občas také nemusí nic brát:

```py
def funkce():     # žádnou hodnotu nebere
	return 42     # vrací vždy 42

print(funkce())   # vypíše 42
```

- občas také nemusí nic vracet:

```py
def funkce():
	print("jen vypisuju, nic neberu ani nevracím")
	
funkce()
```

##### Základní Processing program
- `line(x1, y1, x2, y2)` -- vykreslení čáry
- `rect(x1, y1, x2, y2)` -- vykreslení obdélníku
- `ellipse(x1, y1, x2, y2)` -- vykreslení elipsy

```py
def setup():  # kód, který se vykoná pouze jednou
	size(400, 400)   # nastavení velikosti okna
	background(255)  # nastavení pozadí na bílou

def draw():  # kód, který se dokola opakuje
	line(200, 100, 200, 230)
	line(200, 230, 220, 300)
	line(200, 230, 180, 300)
	line(200, 150, 180, 200)
	line(200, 150, 220, 200)
	ellipse(200, 100, 50, 50)
	rect(-1, 300, 401, 401)
```

1. Přidejte panáčkovi domeček.
2. Přidejte panáčkovi stylový klobouk.

##### Používání proměnných

```py
x = 3   # definování proměnných
y = 20

def setup():
	size(400, 400)

def draw():
	global x, y  # použití proměnných ve funkci
	
	background(255)
	ellipse(x, y, 10, 10)
	
	# posouvaní míčku
	# pokud vyjede mimo obrazovku, vrátíme ho zpět
	x = (x + 3) % width
	y = (y + 5) % height
```

1. Místo posouvání míčku simulujte "odrážení" od stěny. [[řešení](/assets/programovani-je-hra/3.2.1.py)]
	- Přidejte gravitaci. ⭐ [[řešení](/assets/programovani-je-hra/3.2.1-1.py)]
	- Přidejte více míčků. ⭐

##### Operace na canvasu
- `translate(x, y)`: posuň plátno o {% latex %}(x, y){% endlatex %}
- `rotate(radians(r))`: otoč plátno o {% latex %}r{% endlatex %} stupňů
- po konci funkce `draw()` se opět resetuje!

```py
def setup():  # kód, který se vykoná pouze jednou
	size(400, 400)   # nastavení velikosti okna
	background(255)  # nastavení pozadí na bílou

def draw():  # kód, který se dokola opakuje
	translate(width/2, height/2)
	rotate(radians(45))
	translate(-width/2, -height/2)
	
	line(200, 100, 200, 230)
	line(200, 230, 220, 300)
	line(200, 230, 180, 300)
	line(200, 150, 180, 200)
	line(200, 150, 220, 200)
	ellipse(200, 100, 50, 50)
	rect(-1, 300, 401, 401)
```

1. Naprogramuje animaci panáčka, jak:
	- se točí dokola. [[řešení](/assets/programovani-je-hra/3.3.1-1.py)]
	- mává rukou tam a zpět. [[řešení](/assets/programovani-je-hra/3.3.1-2.py)]

### 4. hodina (14. 1. 2021)
1. Naprogramujte vykreslení černobílé {% latex %}8 \times 8{% endlatex %} šachovnice. [[řešení](/assets/programovani-je-hra/4.3.1.py)]

#### Zmáčknutí klávesy

```cpp
def keyPressed():
	if key == 'a':
		# vykoná se po zmáčknutí klávesy 'a'
	else:
		# vykoná se po zmáčknutí jiné klávesy
		
	# pro speciální klávesy jako šipky používejte `keyCode`:
	if keyCode == LEFT:
		# vykoná se po zmáčknutí levé šipky
```

- existuje také `keyReleased`, která značí puštění klávesy

1. Naprogramujte čtverec, který se hýbe po stisknutí `wasd`. [[řešení](/assets/programovani-je-hra/4.1.1-1.py)]
	- udělejte pohyb plynulý (brždění, když pustíme klávesu) ⭐ [[řešení](/assets/programovani-je-hra/4.1.1-2.py)]

#### Zmáčknutí myši
```cpp
def mousePressed():
	if mouseButton == LEFT:
		# vykoná se po zmáčknutí levého tlačítka myši
	elif mouseButton == RIGHT:
		# vykoná se po zmáčknutí pravého tlačítka myši
```

- také je možné využít proměnné `mouseX` a `mouseY`, které udržují pozici kurzoru myši

1. Naprogramujte kruh, který se vždy vykresuje na pozici myši. [[řešení](/assets/programovani-je-hra/4.2.1-1.py)]
	- přidejte pohyb plynulý (aby se kruh plynule přibližoval k myši) [[řešení](/assets/programovani-je-hra/4.2.1-2.py)]

#### Barvičky!
- RGB spektrum -- míchání červené, zelené a modré složky
- `fill(cervena, zelena, modra)` (vždy od `0` do `255`)
- Processing má vestavěný nástroj na výběr barev:
	- `Tools -> Color Selector...`

1. Vytvořte červenou, zelenou, azurovou, bílou, černou, šedou, růžovou barvu.

### 5. hodina (21. 1. 2021)
1. Naprogramujte [Conwayovu „Game of Life“](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) (ovládání myší + klávesami) ⭐. [[řešení](/assets/programovani-je-hra/5.1.1-1.py)]
	- přidejte barvičky! ⭐ [[řešení](/assets/programovani-je-hra/5.1.1-2.py)]
	- přidejte ovládání držením levého/pravého tlačítka [[řešení](/assets/programovani-je-hra/5.1.1-3.py)]

#### Alternativní smyčka
```py
# následující smyčka:
x = 0
while x < 10:
	print(x)
	x += 1

# jde také zapsat jako:
for x in range(0, 10):
	print(x)
```

- zápis je kratší a čitelnější

### 6. hodina (28. 1. 2021)

#### Třídy

{:.rightFloatBox}
<div markdown="1">
**Zajímavost:** metodám tvaru `__jméno__` se  říká „magické.“ Umí s objekty dělat řadu věcí, jako např. definovat, co znamená je sčítat, násobit, apod.
</div>

- **předpisy** věcí -- jaké mají vlastnosti, jak se chovají...
	- příklad: míč/auto/člověk/zvíře...
- specifickým proměnným tříd se říká **objekty**
	- jsou to tzv. instance třídy
- **dědičnost** -- vytváření tříd, které jsou případy jiných:
	- každá další třída **dědí** vlastnosti předka a potenciálně přidává nějaké nové
	- živočich {% latex %}\rightarrow{% endlatex %} obratlovec {% latex %}\rightarrow{% endlatex %} plaz {% latex %}\rightarrow{% endlatex %} krokodýl
	- dopravní prostředek {% latex %}\rightarrow{% endlatex %} vozidlo {% latex %}\rightarrow{% endlatex %} automobil {% latex %}\rightarrow{% endlatex %} elektromobil
	- těleso {% latex %}\rightarrow{% endlatex %} rovnoběžnostěn {% latex %}\rightarrow{% endlatex %} kvádr

```py
# vytvoření třídy, která popisuje lidi
# každý člověk má jméno, věk a umí vyrůst
class Clovek:

	# speciální metoda, která se zavolá, když se objekt vytváří
	def __init__(self, jmeno, vek):
		self.jmeno = jmeno
		self.vek = vek

	# funkce, kterou má každý člověk
	# po zavolání zvýší jeho věk o 1
	def vyrost(self):
		self.vek += 1

# vytvoření objektu (instance třídy Clovek) alice a bob, kteří jsou lidé
alice = Clovek("Alice Novotná", 20)
bob = Clovek("Bořek Stavitel", 34)

# zavolání vlastností na objekty
alice.vyrost()
bob.vyrost()
```

1. Přidejte funkci `vyrost_o`, která bere parametr `o` a přidá danému člověku tolik let. [[řešení](/assets/programovani-je-hra/6.1.1.py)]
2. Přidejte člověku proměnnou `vaha` a funkce `ztloustni` a `zhubni`, které váhu o `1` zvyšují/snižují. [[řešení](/assets/programovani-je-hra/6.1.2.py)]
3. Vytvořte Processing sketch, kde bude po obrazovce létat míče (vytvořené myší). [[řešení](/assets/programovani-je-hra/6.1.3-1.py)]
	- hint: vytvořte třídu `Ptak`, nově vytvořené ptáky ukládejte do pole; každé pole má funkci `append(věc)`, která na jeho konec přidá věc
	- upravte pohyb tak, [aby byl realistický](https://www.youtube.com/watch?v=QbUPfMXXQIY)  ⭐⭐  [[nedokončeno](/assets/programovani-je-hra/6.1.3-2.py)]
		- hint: inspirujte se [tímhle článkem](https://gamedevelopment.tutsplus.com/tutorials/3-simple-rules-of-flocking-behaviors-alignment-cohesion-and-separation--gamedev-3444)

#### Text
```py
def setup():
    size(400, 400)
    background(255)

    fill(0)                    # černý text
    textSize(32)               # velikost textu 32
    textAlign(CENTER, CENTER)  # vycentrování
    
    # vykreslení textu doprostřed obrazovky
    text('Ahoj!', width / 2, height / 2)
```

### 7. hodina (11. 2. 2021)
1. Naprogramujte hru „Flappy bird“ ⭐⭐ [[aktuální stav](/assets/programovani-je-hra/7.1.1.py)] [[+kolize](/assets/programovani-je-hra/7.1.2.py)] [[+grafika +gravitace](/assets/programovani-je-hra/7.1.3.py)]

#### Knihovny
- používání kódu (funkcí, proměnných), který naprogramovali ostatní
- syntax:
	- naimportování knihovny: `import <jméno knihovny>`
	- používání věcí z knihovny: `<jméno knihovny>.věc`

##### `math`
- matematika-related věci
- funkce:
	- `math.sin`, `math.cos`, `math.tan`
	- `math.log`aritmus, `math.factorial`
	- ...
- konstanty:
	- `math.pi`, `math.e`

##### `random`
- generování náhodných čísel:
	- `math.randint(a, b)` -- náhodné **celé** číslo od `a` do `b`
	- `math.random()` -- náhodné **desetinné** číslo od `0` do `1`

#### Docstringy
- způsob komentování toho, co dělá celá funkce
- automaticky z něj lze vygenerovat dokumentaci ke knihovně, ve které je
- pomáhá pokročilejším prostředím 

```py
def moje_funkce():
	"""Tahle moje funkce dělá moc cool věci."""
	# ...
	# kód funkce
	# ...
```

### 8. hodina (18. 2. 2021)

#### `str`ingy
- proměnné typu `str` v sobě ukládají text
- věci, které string nejsou, lze na string převést přes funkci `str`
- string lze přímo z textu vytvořit buďto `'takhle'`, nebo `"takhle"`

```py
a = "Tohle je hezká věta."       # normální string
b = "Tohle" + " je " + "další."  # spojování více stringů do jednoho
c = "5^420 = " + str(5 ** 420)   # spojování a převádění čísel na string

print(a)
print(b)
print(c)
```

### 9. hodina (25. 2. 2021)


#### rekurze
- funkce, která odkazuje „sama na sebe“
- dokáže výrazně zjednodušit kód

```py
def factorial(n):
	if n == 0:    # tzv. "base case" -- místo, kde se rekurze zastaví
		return 1
	else:
		# vycházíme z toho, že n * (n - 1)! = n!
		return n * factorial(n - 1)

print(factorial(5))
```

1. Naprogramujte [Fibonacciho čísla](https://en.wikipedia.org/wiki/Fibonacci_number) a porovnejte rychlost:
	- iterativně (smyčka) [[řešení](/assets/programovani-je-hra/9.1.1.1.py)]
	- rekurzivně [[řešení](/assets/programovani-je-hra/9.1.1.2.py)]
2. Naprogramujte [Hanoiské věže](https://en.wikipedia.org/wiki/Tower_of_Hanoi). ⭐ [[řešení](/assets/programovani-je-hra/9.1.2.py)]

---

1. Naprogramujte [Sierpińského trojúhelník](https://cs.wikipedia.org/wiki/Sierpińského_trojúhelník) [[řešení](/assets/programovani-je-hra/9.2.1.py)]
2. Naprogramujte [Mengerovu houbu](https://cs.wikipedia.org/wiki/Mengerova_houba) ve 2D. [[řešení](/assets/programovani-je-hra/9.2.2.py)]

### Materiály

#### [Python](https://www.python.org/downloads/)
- [Python Tutor](http://www.pythontutor.com/visualize.html) -- vizualizér Python kódu, ze kterého je hezky vidět, co program dělá.
- [Repl.it pro Python](https://repl.it/languages/python3) -- prostředí, ve kterém budeme programovat.
- [Processing 3](https://processing.org/) -- grafické prostředí, ve kterém budeme pracovat.
	- [Processing 3 Reference](https://py.processing.org/reference/) -- dokumentace k Processingu
- [Ponořme se do Pythonu](http://diveintopython3.py.cz/index.html) -- dobře napsaná kniha o programování v Pythonu 3, na kterou se můžete podívat, pokud byste se rádi Python učili i ve svém volném čase.
- [PyCharm](https://www.jetbrains.com/pycharm/) -- nejlepší Python IDE

#### Programování
- [Advent Kódu](https://adventofcode.com/) -- stránka, kde je na každý den adventu programovací úloha
- [The Coding Train](https://thecodingtrain.com/CodingChallenges/) -- videa o programování různých vizualizací v Processingu

#### Algoritmy, datové struktury
- [Korespondenční Seminář z Programování](http://ksp.mff.cuni.cz/z/) -- skvělý způsob, jak se na zajímavých úlohách naučit programovat a poznat při tom nové kamarády 🙂.
- [Průvodce labyrintem algoritmů](http://pruvodce.ucw.cz/) -- úžasná příručka pro ty, kteří by se něco rádi dozvěděli o algoritmech a datových strukturách.

{:.center}
![Programování v kostce.](/assets/programovani-je-hra/turtles.png)

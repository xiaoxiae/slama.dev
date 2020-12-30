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
c = True              # krabička c, která drží „pravdu“
d = a                 # krabička d, která si uloží, co je v a

# print(...) vypíše cokoliv, co do něho dáte
# pro nás zatím magie
print(a)
print(b)
print(c)
print(d)
```

- jméno krabičky může obsahovat:
	- velká a malá písmena
	- čísla (ale ne jako první znak!)
	- symbol `_`

```python
123 = 1   # neplatné, jméno nesmí začínat číslem
a+b = 123 # neplatné, jméno nesmí obsahovat +
```

1. Vytvořte proměnné `a`, `b`, `c` tak, aby každá obsahovala jiný typ informací.
2. Máte číselné proměnné `a` a `b`. Napište program, který prohodí jejich obsah.
	* Zvládnete to bez použití pomocné proměnné (a bez použití `a, b = b, a`)? ⭐

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

```python
a = 12 + 6 - 5   # a = 13
b = a / 2        # b = 6.5
c = -b           # c = -6.5
d = 2 + 2 * 2    # d = 6
e = (2 + 2) * 2  # d = 8

print(a)
print(b)
print(c)
print(d)
print(e)
```

1. Máte proměnnou `a`, která udává délku strany kostky. Vypište její obsah.
	* Vypište její plochu {% latex %}(2b){% endlatex %}.
	* Vypište plochu největší koule, která se do kostky vejde.
	* Vypište plochu největší koule, do které se kostka vejde. ⭐
2. Máte proměnnou `celsius` s číselnou hodnotou. Vypište, kolik je to Fahrenheitů ([odkaz na Wiki](https://cs.wikipedia.org/wiki/Stupeň_Fahrenheita), pokud nevíte, jak převod vypadá).

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

1. Máte číselné proměnné `a` a `b`. Vypište `<`, `>` nebo `=` podle toho, zda je `a` menší/větší/rovné.
2. Máte číselnou proměnnou `a`. Napište program, který vypíše `Sudé!` když je `a` sudé a `Liché!`, když je `a` liché. Použijte operátor `%` (zbytek po dělení).
	- Zvládnete to i bez operátoru `%`?
3. Máte číselné proměnné `a`, `b` a `c`, které mají různé hodnoty. Vypište tato čísla od nejmenšího po největší. Využijte toho, že `if`y mohou být vnořené. ⭐

### 2. hodina (17. 12. 2020)

#### Uživatelský vstup
- čtení věcí, které uživatelé zadají

```py
veta  = input()       # čtení věty
cislo = int(input())  # čtení čísla

print(veta)
print(cislo)
```

1. Chceme se uživatele zeptat, kolik mu je let. Vypište jeho věk a pokud mu je více než 20, napište `Je ti více než 20!`.

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

1. Máte číselnou proměnnou `a`. Vypište všechna čísla od {% latex %}1{% endlatex %} do `a`.
	* Vypište jen sudá čísla {% latex %}(2b){% endlatex %}.
2. Máte číselnou proměnnou `a`. Vypište všechna čísla, která dělí `a`.
	* Vypište její prvočíselný rozklad. ⭐
3. Chceme napsat robota, který bude hádat čísla od {% latex %}1{% endlatex %} do {% latex %}100{% endlatex %}. Uživateli řekne číslo, které hádá, a zeptá se ho, zda je uživatelovo menší, nebo větší. ⭐

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
	- počet čísel v poli. {% latex %}(1b){% endlatex %}
	- největší číslo v poli. {% latex %}(1b){% endlatex %}
	- nejmenší číslo v poli. {% latex %}(1b){% endlatex %}
	- součet čísel v poli. {% latex %}(1b){% endlatex %}

### Dodatečné materiály

- [Python Tutor](http://www.pythontutor.com/visualize.html) -- vizualizér Python kódu, ze kterého je hezky vidět, co program dělá.
- [Repl.it pro Python](https://repl.it/languages/python3) -- prostředí, ve kterém budeme programovat.
- [Python 3](https://www.python.org/downloads/) -- webovky jazyka, ve kterém budeme programovat.
- [Ponořme se do Pythonu](http://diveintopython3.py.cz/index.html) -- dobře napsaná kniha o programování v Pythonu 3, na kterou se můžete podívat, pokud byste se rádi Python učili i ve svém volném čase.
- [Korespondenční Seminář z Programování](http://ksp.mff.cuni.cz/z/) -- skvělý způsob, jak se na zajímavých úlohách naučit programovat a poznat při tom nové kamarády 🙂.
- [Průvodce labyrintem algoritmů](http://pruvodce.ucw.cz/) -- super příručka pro ty, kteří by se něco rádi dozvěděli o algoritmech a datových strukturách, do hloubky.
- [Advent Kódu](https://adventofcode.com/) -- stránka, kde na každý den je lehčí a těžší úloha, která se řeší s pomocí programování. Každoročně řeším a velice doporučuji!

{:.center}
![Programování v kostce.](/assets/programovani-je-hra/turtles.png)

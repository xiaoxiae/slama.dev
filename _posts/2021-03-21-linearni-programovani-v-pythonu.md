---
language: cz
title: Lineární programování v Pythonu
---


- .
{:toc}

### Úvodní informace
Tato stránka obsahuje náhodné programy ze cvičení/přednášky předmětu Lineární programování a kombinatorická optimalizace. Ke spuštění programů je potřeba nainstalovat Pythoní knihovnu `pulp` (přes `pip install pulp`), kterou k řešení problémů používám.

Pokud s `pulp`em také vyřešíte nějaký problém, tak budu moc rád za email/pull request, ať tu máme příkladů co možná nejvíce 🙂.

### Praktické příklady

#### Problém pekárny
Pekárna má k dispozici {% latex %}5{% endlatex %} kilo mouky, {% latex %}125{% endlatex %} vajec a půl kila soli. Za jeden chleba zı́ská pekárna {% latex %}20{% endlatex %} korun, za housku {% latex %}2{% endlatex %} koruny, za bagetu {% latex %}10{% endlatex %} korun a za koblihu {% latex %}7{% endlatex %} korun. Pekárna se snažı́ vydělat co nejvı́ce. Jak ale zjistı́ kolik chlebů, housek, baget a koblih má upéci?

```py
from pulp import *

# vytvoření modelu
model = LpProblem(name="problem-pekarny", sense=LpMaximize)

# proměnné -- kolik housek a chlebů upečeme
xc = LpVariable(name="chleby", lowBound=0, cat='Integer')
xh = LpVariable(name="housky", lowBound=0, cat='Integer')
xb = LpVariable(name="bagety", lowBound=0, cat='Integer')
xk = LpVariable(name="koblihy", lowBound=0, cat='Integer')

# omezení -- nesmíme na pečení spotřebovat více surovin než máme
model += 500 * xc + 150 * xh + 230 * xb + 100 * xk <= 5000
model +=  10 * xc +   2 * xh +   7 * xb + xk       <= 125
model +=  50 * xc +  10 * xh +  15 * xb            <= 500

# funkce k maximalizaci -- zisk z pečení
model += 20 * xc + 2 * xh + 10 * xb + 7 * xk

# řešení (ignorujeme debug zprávy)
status = model.solve(PULP_CBC_CMD(msg=False))
print(int(xc.value()), int(xh.value()), int(xb.value()), int(xk.value()))
```

#### Problém batohu
Zformulujte Problém batohu pomocı́ celočı́sleného lineárnı́ho programovánı́. Tedy pro {% latex %}n{% endlatex %} předmětů, kde {% latex %}i{% endlatex %}-tý má nějakou váhu {% latex %}v_i{% endlatex %} a cenu {% latex %}c_i{% endlatex %}, máme batoh s danou nosnostı́ {% latex %}V{% endlatex %} a my se do něj snažı́me naskládat předměty tak, abychom maximalizovali celkovou cenu předmětů v batohu.

```py
from pulp import *

data = [
        { 'nosnost': 165,
          'hmotnosti': [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
          'ceny': [92, 57, 49, 68, 60, 43, 67, 84, 87, 72] },
        { 'nosnost': 26,
          'hmotnosti': [12, 7, 11, 8, 9],
          'ceny': [24, 13, 23, 15, 16] },
        { 'nosnost': 6404180,
          'hmotnosti': [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684],
          'ceny': [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261] },
        ]

for dataset in data:
    size = len(dataset['hmotnosti'])

    # vytvoření modelu
    model = LpProblem(name="problem-batohu", sense=LpMaximize)

    # proměnné -- zda do batohu vložíme i-tou proměnnou
    variables = [LpVariable(name=f"x{i}", cat='Binary') for i in range(size)]

    # omezení -- nesmíme do batohu vložit více než nosnost
    model += lpSum([dataset['hmotnosti'][i] * variables[i] for i in range(size)]) <= dataset['nosnost']

    # funkce k maximalizaci -- cena věcí v batohu
    model += lpSum([dataset['ceny'][i] * variables[i] for i in range(size)])

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("cena batohu:", model.objective.value())
    print("vezmeme:", *[int(variables[i].value()) for i in range(size)])
    print()
```

### Zdroje/materiály
- [Hands-On Linear Programming: Optimization With Python](https://realpython.com/linear-programming-python/)

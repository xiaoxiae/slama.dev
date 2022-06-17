from pulp import *
from itertools import *

data = [
    ([2, 3, 8, 7, 5, 2], [10, 9, 5, 3],
    [[1, 3, 2, 4],
     [2, 2, 1, 3],
     [2, 3, 1, 3],
     [2, 4, 0, 0],
     [1, 5, 1, 2],
     [3, 4, 1, 2]]),
]

for p, o, c in data:
    # počet pekáren, počet obchodů
    n = len(p)
    m = len(o)

    # vytvoření modelu
    model = LpProblem(name="1-a", sense=LpMinimize)

    # proměnné -- x_{ij}, kolik i-tá pekárna doveze j-tému obchodu
    # proměnné jsou celočíselné a nezáporné
    x = []
    for i in range(n):
        x.append([])
        for j in range(m):
            x[-1].append(LpVariable(name=f"x_{i}_{j}", lowBound=0, cat='Integer'))

    # omezení
    ## každá pekárna rozveze všechny rohlíky
    for i in range(n):
        model += p[i] == lpSum([x[i][j] for j in range(m)])

    ## každý obchod získá potřebné rohlíky
    for i in range(m):
        model += o[i] == lpSum([x[j][i] for j in range(n)])

    # funkce k minimalizaci -- náklady
    model += lpSum([x[i][j] * c[i][j] for i in range(n) for j in range(m)])

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("náklady:", int(model.objective.value()))
    for i in range(n):
        for j in range(m):
            print(int(int(x[i][j].value())), "\t", end="")
        print()
    print()

from pulp import *
from itertools import *

data = [
    (
        [2, 3, 8, 7, 5, 2],
        [10, 9, 5, 3],
        [
            [1, 3, 2, 4],
            [2, 2, 1, 3],
            [2, 3, 1, 3],
            [2, 4, 0, 0],
            [1, 5, 1, 2],
            [3, 4, 1, 2],
        ],
        [
            [10, 3, 2, 1],
            [1, 3, 2, 3],
            [3, 1, 2, 2],
            [1, 2, 2, 3],
            [2, 2, 2, 4],
            [6, 4, 2, 1],
        ],
    ),
]

for p, o, c, l in data:
    # počet pekáren, počet obchodů
    n = len(p)
    m = len(o)

    # vytvoření modelu
    model = LpProblem(name="1-a", sense=LpMinimize)

    # proměnné -- x_{ijk}, zda i-tá pekárna doveze j-tému obchodu k rohlíků
    x = []
    for i in range(n):
        x.append([])
        for j in range(m):
            x[-1].append([])
            for k in range(p[i] + 1):
                x[-1][-1].append(LpVariable(name=f"x_{i}_{j}_{k}", cat="Binary"))

    # omezení
    ## nerozvážíme např. 2 a 3 rohlíky individuálně
    for i in range(n):
        for j in range(m):
            model += lpSum([x[i][j][k] for k in range(p[i] + 1)]) == 1

    ## každá pekárna rozveze všechny rohlíky
    for i in range(n):
        model += p[i] == lpSum(
            [k * x[i][j][k] for j in range(m) for k in range(p[i] + 1)]
        )

    ## každý obchod získá potřebné rohlíky
    for i in range(m):
        model += o[i] == lpSum(
            [k * x[j][i][k] for j in range(n) for k in range(p[j] + 1)]
        )

    # funkce k minimalizaci -- náklady
    model += lpSum(
        [
            k * x[i][j][k] * c[i][j]
            for i in range(n)
            for j in range(m)
            for k in range(p[i] + 1)
        ]
    ) + lpSum(
        [
            x[i][j][k] * l[i][j]
            for i in range(n)
            for j in range(m)
            for k in range(1, p[i] + 1)
        ]
    )

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("náklady:", int(model.objective.value()))
    for i in range(n):
        for j in range(m):
            for k in range(p[i] + 1):
                if x[i][j][k].value() == 1:
                    print(k, "\t", end="")
                    break
        print()
    print()

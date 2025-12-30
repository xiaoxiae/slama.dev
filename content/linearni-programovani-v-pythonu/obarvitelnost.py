from pulp import *

# seznamy (neorientovaných!) hran grafů
edges_lists = [
    # K_5
    [(1, 2), (3, 2), (2, 4), (3, 4), (5, 4), (3, 5), (1, 5), (2, 5), (3, 1), (1, 4)],
    # skoro K_6
    [
        (1, 2),
        (1, 3),
        (4, 3),
        (4, 5),
        (6, 5),
        (6, 2),
        (6, 1),
        (6, 4),
        (1, 4),
        (2, 5),
        (2, 3),
        (3, 5),
    ],
    # cesta
    [(1, 2), (3, 2), (3, 4), (4, 5), (5, 6)],
]

for edges in edges_lists:
    # počet vrcholů
    n = len(set([u for u, v in edges] + [v for u, v in edges]))

    # vytvoření modelu
    model = LpProblem(name="chromaticke-cislo", sense=LpMinimize)

    # proměnné -- x[i][k] podle toho, zda je i-tý vrchol obarvený k-tou barvou
    # proměnná navíc ještě bude chromatické číslo
    chromatic_number = LpVariable(name="chromatic number", lowBound=0, cat="Integer")
    variables = []
    for i in range(n):
        variables.append([])
        for j in range(n):
            variables[-1].append(LpVariable(name=f"x_{i}_{j}", cat="Binary"))

    # omezení
    ## každý vrchol má právě jednu barvu
    for i in range(n):
        model += lpSum(variables[i]) == 1

    ## pro každou hranu platí, že její sousední vrcholy nemají stejnou barvu
    for u, v in edges:
        for color in range(n):
            model += variables[u - 1][color] + variables[v - 1][color] <= 1

    ## navíc chceme, aby chromatic_number bylo číslo nejvyšší použité barvy
    for i in range(n):
        variables.append([])
        for j in range(n):
            model += chromatic_number >= (j + 1) * variables[i][j]

    # minimalizujeme chromatické číslo
    model += chromatic_number

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))
    print("chromatické číslo:", int(chromatic_number.value()))
    for i in range(n):
        for j in range(n):
            if variables[i][j].value() != 0:
                print(f"vrchol {i}: barva {j}")
    print()

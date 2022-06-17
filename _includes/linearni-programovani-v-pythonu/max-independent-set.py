from pulp import *

# seznamy (neorientovaných!) hran grafů
edges_lists = [
    # K_5
    [(1, 2), (3, 2), (2, 4), (3, 4), (5, 4), (3, 5), (1, 5), (2, 5), (3, 1), (1, 4)],
    # skoro K_6
    [(1, 2), (1, 3), (4, 3), (4, 5), (6, 5), (6, 2), (6, 1), (6, 4), (1, 4), (2, 5), (2, 3), (3, 5)],
    # cesta
    [(1, 2), (3, 2), (3, 4), (4, 5), (5, 6)],
]

for edges in edges_lists:
    # počet vrcholů
    n = len(set([u for u, v in edges] + [v for u, v in edges]))

    # vytvoření modelu
    model = LpProblem(sense=LpMaximize)

    # proměnné -- x[i] podle toho, zda vyberem i-tý vrchol
    variables = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(n)]

    # omezení
    ## každá hrana musí být pokryta nejvýše jednou
    for u, v in edges:
        model += variables[u - 1] + variables[v - 1] <= 1

    # minimalizujeme počet vybraných vrcholů
    model += lpSum(variables)

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))
    print("vybrané vrcholy: ", end="")
    for i in range(n):
        print(int(variables[i].value()), end=" ")
    print()

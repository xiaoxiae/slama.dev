from pulp import *
from itertools import *

bins_lists = [
    (100, [70, 60, 50, 33, 33, 33, 11, 7, 3]),
    (100, [99, 94, 79, 64, 50, 46, 43, 37, 32, 19, 18, 7, 6, 3]),
    (100, [49, 41, 34, 33, 29, 26, 26, 22, 20, 19]),
    (524, [442, 252, 252, 252, 252, 252, 252, 252, 127, 127, 127, 127, 127, 106, 106, 106, 106, 85, 84, 46, 37, 37, 12, 12, 12, 10, 10, 10, 10, 10, 10, 9, 9]),
]

for maximum_bin_load, weights in bins_lists:
    # počet objektů
    n = len(weights)

    # vytvoření modelu
    model = LpProblem(name="bin-packing", sense=LpMinimize)

    # proměnné -- binární x_{i, j}, zda i-tý objekt patří do j-tého koše
    # proměnná navíc ještě bude počet košů
    bin_count = LpVariable(name="bin count", lowBound=0, cat='Integer')
    variables = []
    for i in range(n):
        variables.append([])
        for j in range(n):
            variables[-1].append(LpVariable(name=f"x_{i}_{j}", cat='Binary'))

    # omezení
    ## v každém koši je nejvýše tolik, kolik toho unese
    for j in range(n):
        model += lpSum([variables[i][j] * weights[i] for i in range(n)]) <= maximum_bin_load

    ## každý předmět byl umístěn do právě jednoho koše
    for i in range(n):
        model += lpSum([variables[i][j] for j in range(n)]) == 1

    ## navíc chceme, aby bin_count byl počet košů, tzn. je větší
    for i in range(n):
        for j in range(n):
            model += bin_count >= (j + 1) * variables[i][j]

    # funkce k minimalizaci -- počet košů
    model += bin_count

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("počet košů:", int(bin_count.value()))
    for i in range(n):
        for j in range(n):
            if variables[i][j].value() != 0:
                print(f"předmět {i} (váha {weights[i]}): koš {j}")
    print()

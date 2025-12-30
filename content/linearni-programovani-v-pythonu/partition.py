from pulp import *
from itertools import *

bins_lists = [
    [2, 10, 3, 8, 5, 7, 9, 5, 3, 2],
    [771, 121, 281, 854, 885, 734, 486, 1003, 83, 62],
    [484, 114, 205, 288, 506, 503, 201, 127, 410],
    [19, 17, 13, 9, 6],
    [3, 4, 3, 1, 3, 2, 3, 2, 1],
]

for weights in bins_lists:
    # počet objektů
    n = len(weights)

    # vytvoření modelu
    model = LpProblem(name="bin-packing", sense=LpMinimize)

    # proměnné -- binární x_i, zda i-tý objekt patří do jedné nebo druhé části
    variables = [LpVariable(name=f"x_{i}", cat="Binary") for i in range(n)]

    # omezení
    ## součet obou částí se rovná
    model += lpSum([variables[i] * weights[i] for i in range(n)]) == lpSum(
        [(1 - variables[i]) * weights[i] for i in range(n)]
    )

    # funkce k minimalizaci -- nic! jedná se o rozhodovací problém

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("velikost:", sum([int(variables[i].value()) * weights[i] for i in range(n)]))
    for i in range(n):
        print(int(variables[i].value()), weights[i])
    print()

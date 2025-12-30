from pulp import *
from itertools import *

distance_lists = [
    [
        [0],
        [3, 0],
        [4, 4, 0],
        [2, 6, 5, 0],
        [7, 3, 8, 6, 0],
    ],
    [
        [0],
        [29, 0],
        [82, 55, 0],
        [46, 46, 68, 0],
        [68, 42, 46, 82, 0],
        [52, 43, 55, 15, 74, 0],
        [72, 43, 23, 72, 23, 61, 0],
        [42, 23, 43, 31, 52, 23, 42, 0],
        [51, 23, 41, 62, 21, 55, 23, 33, 0],
        [55, 31, 29, 42, 46, 31, 31, 15, 29, 0],
        [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0],
        [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0],
        [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0],
        [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0],
        [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0],
    ],
    [
        [0],
        [633, 0],
        [257, 390, 0],
        [91, 661, 228, 0],
        [412, 227, 169, 383, 0],
        [150, 488, 112, 120, 267, 0],
        [80, 572, 196, 77, 351, 63, 0],
        [134, 530, 154, 105, 309, 34, 29, 0],
        [259, 555, 372, 175, 338, 264, 232, 249, 0],
        [505, 289, 262, 476, 196, 360, 444, 402, 495, 0],
        [353, 282, 110, 324, 61, 208, 292, 250, 352, 154, 0],
        [324, 638, 437, 240, 421, 329, 297, 314, 95, 578, 435, 0],
        [70, 567, 191, 27, 346, 83, 47, 68, 189, 439, 287, 254, 0],
        [211, 466, 74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145, 0],
        [268, 420, 53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202, 57, 0],
        [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483, 0],
        [121, 518, 142, 84, 297, 35, 29, 36, 236, 390, 238, 301, 55, 96, 153, 336, 0],
    ],
]

for distances in distance_lists:
    # počet měst
    n = len(distances)

    # vytvoření modelu
    model = LpProblem(name="tsp", sense=LpMinimize)

    # proměnné -- binární x_{i, j} podle toho, zda je tato hrana na cestě
    # jsou symetrické a vždy i >= j
    variables = []
    for i in range(n):
        variables.append([])
        for j in range(i + 1):
            variables[-1].append(LpVariable(name=f"x_{i}_{j}", cat="Binary"))

    # omezení
    ## z každého vrcholu jedna hrana vychází a jedna do něj přichází
    for i in range(n):
        model += (
            lpSum([variables[i if i > j else j][j if i > j else i] for j in range(n)])
            == 2
        )
        model += variables[i][i] == 0

    ## z každé podmnožiny vrcholů vychází alespoň jedna hrana
    for size in range(1, n - 1):  # TODO: maybe not
        for subset in combinations(range(n), r=size):
            model += (
                lpSum(
                    [
                        variables[i if i > j else j][j if i > j else i]
                        for i in subset
                        for j in range(n)
                        if j not in subset
                    ]
                )
                >= 1
            )

    # funkce k minimalizaci -- vzdálenosti kružnice
    model += lpSum(
        [
            variables[i][j] * distances[i][j]
            for i, j in product(range(n), repeat=2)
            if i > j
        ]
    )

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("minimální cesta: ", int(model.objective.value()))
    for i in range(n):
        for j in range(n):
            print(
                int(variables[i if i > j else j][j if i > j else i].value()),
                " ",
                end="",
            )
        print()
    print()

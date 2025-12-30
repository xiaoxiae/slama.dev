from pulp import *

graphs = [
    [
        "Complete graph on 5 vertices",
        [0, 1, 2, 3, 4],
        [
            (0, 1),
            (2, 1),
            (1, 3),
            (2, 3),
            (4, 3),
            (2, 4),
            (0, 4),
            (1, 4),
            (2, 0),
            (0, 3),
        ],
    ],
    [
        "Path of 6 vertices",
        [0, 1, 2, 3, 4, 5],
        [(0, 1), (2, 1), (2, 3), (3, 4), (4, 5)],
    ],
    [
        "Petersen graph",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [
            (0, 1),
            (0, 4),
            (0, 5),
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 7),
            (3, 4),
            (3, 8),
            (4, 9),
            (5, 7),
            (5, 8),
            (6, 8),
            (6, 9),
            (7, 9),
        ],
    ],
]

for name, vertices, edges in graphs:
    n = len(vertices)

    model = LpProblem(sense=LpMaximize)

    # variables - x[i] binary based on if the i-th vertex is in the set
    variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]

    # inequalities
    ## each edge must have at most one vertex from the set
    for u, v in edges:
        model += variables[u - 1] + variables[v - 1] <= 1

    # minimize the number of selected edges
    model += lpSum(variables)

    status = model.solve(PULP_CBC_CMD(msg=False))

    print(name + "\n" + "-" * len(name))
    print("set size =", int(model.objective.value()))

    for i in range(n):
        print(int(variables[i].value()), end=" ")
    print()
    print()

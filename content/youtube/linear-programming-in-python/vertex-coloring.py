from pulp import *

# three graphs, given as an edge list
# we're assuming that vertices are index 0 to n-1
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

    # note: this is a minimization problem, so we use LpMinimize!
    model = LpProblem(sense=LpMinimize)

    # n^2 variables, where x[i][k] signifies if the i-th vertex is colored with the k-th color
    variables = [
        [LpVariable(name=f"x_{i}_{j}", cat=LpBinary) for j in range(n)]
        for i in range(n)
    ]

    # one more variable - the chromatic number itself
    chromatic_number = LpVariable(name="chromatic number", cat="Integer")

    # inequalities
    # each vertex has exactly one color
    for u in range(n):
        model += lpSum(variables[u]) == 1

    # adjacent edge colors are different
    for u, v in edges:
        for k in range(n):
            model += variables[u][k] + variables[v][k] <= 1

    # we also restrict the chromatic number to be the number of the highest used color
    for u in range(n):
        for k in range(n):
            model += chromatic_number >= (k + 1) * variables[u][k]

    # objective function - minimize the chromatic number
    model += chromatic_number

    status = model.solve(PULP_CBC_CMD(msg=False))

    print(name + "\n" + "-" * len(name))
    print("k =", int(chromatic_number.value()))

    for u in range(n):
        for k in range(n):
            if variables[u][k].value() != 0:
                print(f"v_{u} has color {k + 1}")
    print()

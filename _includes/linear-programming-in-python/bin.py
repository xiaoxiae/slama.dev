from pulp import *
from itertools import *

bin_sets = [
    ("Set 1", 100, [70, 60, 50, 33, 33, 33, 11, 7, 3]),
    ("Set 2", 100, [99, 94, 79, 64, 50, 46, 43, 37, 32, 19, 18, 7, 6, 3]),
    ("Set 3", 100, [49, 41, 34, 33, 29, 26, 26, 22, 20, 19]),
    ("Set 4", 524, [442, 252, 252, 252, 252, 252, 252, 252, 127, 127, 127, 127, 127, 106, 106, 106, 106, 85, 84, 46, 37, 37, 12, 12, 12, 10, 10, 10, 10, 10, 10, 9, 9]),
]

for name, maximum_bin_load, weights in bin_sets:
    n = len(weights)

    model = LpProblem(sense=LpMinimize)

    # variables - binary x[i][j] based on if the i-th item is in the j-th bin
    variables = [
        [LpVariable(name=f"x_{i}_{j}", cat=LpBinary) for j in range(n)]
        for i in range(n)
    ]

    # ... and also the number of bins
    bin_count = LpVariable(name="bin count", cat=LpInteger)

    # inequalities
    ## each bin doesn't contain more than its maximum load
    for j in range(n):
        model += lpSum([variables[i][j] * weights[i] for i in range(n)]) <= maximum_bin_load

    ## each item must be placed in exactly one bin
    for i in range(n):
        model += lpSum([variables[i][j] for j in range(n)]) == 1

    ## we also want the bin count to be the highest bin number
    for i in range(n):
        for j in range(n):
            model += bin_count >= (j + 1) * variables[i][j]

    # objective function - number of bins
    model += bin_count

    status = model.solve(PULP_CBC_CMD(msg=False))

    print(name + "\n" + "-" * len(name))
    print("bin count:", int(bin_count.value()))
    for i in range(n):
        for j in range(n):
            if variables[i][j].value() != 0:
                print(f"item {i} (weight {weights[i]}): bin {j}")
    print()

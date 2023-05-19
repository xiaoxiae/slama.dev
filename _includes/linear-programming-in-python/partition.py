from pulp import *
from itertools import *

weight_sets = [
    ("Set 1", [19, 17, 13, 9, 6]),
    ("Set 2", [3, 4, 3, 1, 3, 2, 3, 2, 1, 5]),
    ("Set 3", [2, 10, 3, 8, 5, 7, 9, 5, 3, 2]),
    ("Set 4", [771, 121, 281, 854, 885, 734, 486, 1003, 83, 62]),
    ("Set 5", [484, 114, 205, 288, 506, 125, 503, 201, 127, 410, 312, 132, 312, 542]),
]

for name, weights in weight_sets:
    n = len(weights)

    model = LpProblem(sense=LpMinimize)

    # variables - binary x[i] based on if the item belongs to the first partition
    variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]

    # ... and also the difference between the left and right side
    difference = LpVariable(name=f"difference", lowBound=0, cat=LpInteger)

    # inequalities
    ## the difference of the parts equals their difference (variable)
    model += difference == lpSum([variables[i] * weights[i] for i in range(n)]) \
            - lpSum([(1 - variables[i]) * weights[i] for i in range(n)])

    # objective function - minimize the difference between the sides
    model += difference

    status = model.solve(PULP_CBC_CMD(msg=False))

    print(name + "\n" + "-" * len(name))
    print("difference:", difference.value())
    for i in range(n):
        print(int(variables[i].value()), end=" ")
    print()
    print()

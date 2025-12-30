def h(n, z, do):
    if n == 0:
        return

    odkladni = 3 - z - do

    h(n - 1, z, odkladni)
    print("Přesouváme " + str(z) + " na " + str(do))
    h(n - 1, odkladni, do)


def hanoi(n):
    """Pro n vypíše postup řešení Hanoiských věží o n discích."""
    h(n, 0, 2)


hanoi(10)

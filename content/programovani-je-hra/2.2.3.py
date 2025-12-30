lo = 1
hi = 100

while lo < hi:
    avg = (lo + hi) // 2

    # magie, abych mohl do stringů dávat přímo proměnné
    print(f"Mám číslo {avg}.")

    odpoved = input("Je číslo větší (napiš >), menší (napiš <), nebo rovné (napiš =): ")

    if odpoved == "<":
        hi = avg
    elif odpoved == ">":
        lo = avg + 1
    elif odpoved == "=":
        print(f"Vyhrál jsem, tvoje číslo je {lo}.")
        quit()
    else:
        print("Odpověz prosím <, > nebo =.")

print("Podvádíš!")

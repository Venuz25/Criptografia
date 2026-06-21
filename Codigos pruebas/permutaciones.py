
def inv_per(permutacion):
    inversa = [0] * len(permutacion)

    for i in range(len(permutacion)):
        inversa[permutacion[i] - 1] = i + 1
    return inversa

permutacion = [3,1,5,2,4]
print(inv_per(permutacion))
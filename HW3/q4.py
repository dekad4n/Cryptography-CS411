from sympy import factorint


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u*q, y-v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

N = 15220196297956469159
C = 6092243189299681137
e = (2**16) + 1
primeFactorsDict = factorint(N)

listPrimeFactors = [n for n in primeFactorsDict.keys()]

p,q = listPrimeFactors[0], listPrimeFactors[1]

phi = (p-1) * (q-1)

d = modinv(e, phi)

p = pow(C, d, N)

## ANSWER
print(p)


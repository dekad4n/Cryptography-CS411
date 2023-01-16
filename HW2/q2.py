import client as cl
from sympy import isprime
from sympy.ntheory import factorint
from myntl import modinv, gcd

# Function I got from stackoverflow.com
def bin2text(s): return "".join(
    [chr(int(s[i:i+8], 2)) for i in range(0, len(s), 8)])
# check if prime, but since numbers are large, do not use sympy
def isPrime(n):
    print(factorint(n))
    return len(factorint(n)) == 1
e,c = cl.getQ2()

p = 129711420978537746088867309342132426785901989689874594485896371555019986573705426172788805726178509467748040679168734095884433597017604012172054368990172572715857537355524013819947862920969421702067385445122242673064958991968666138544380365520456029952414962028711806175784928131826127885820644091951344318387

q = 174066672405085972657808881778978520582809763235147358374332409966322987290745416405220414323004782906757362579157117914494927198442645581197584273451379119673753279114693557694861941678350357667191083878100828920198503774539271289263633646647364198130180304138099281532660260760636194367337370132530987351081

## BOTH primes so we can use phi(n) = (p-1)(q-1)
#print(isprime(p))
#print(isprime(q))
phi = (p-1)*(q-1)

d = modinv(e, phi) 

# gcd(c, n) = 1
print(gcd(c, (p*q)))
# c^x = m
# find x
# c^x = c^d
# since
# then c^d = m
n = p*q
m = pow(c ,d, mod=n)
#print(m)
# now we can generate string!
res = "0" + bin(m)[2:] 


def bin2ASCII(msg):
    res = list()
    for i in range(len(msg)//8):
        bins = msg[:8]
        str_bin = ''.join(str(x) for x in bins)
        res.append(chr(int(str_bin, 2)))
        msg = msg[8:]
    return "".join(res)
a = bin2ASCII(res)
print(bin2ASCII(res))

cl.checkQ2(a)








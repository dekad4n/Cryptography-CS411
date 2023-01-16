import VALUES_Q1 as vals
from decimal import Decimal, getcontext
import math
N, C, e = vals.N, vals.C, vals.e

getcontext().prec = 30000

v = Decimal(C)

## We know that M << N 
## Then 17th power never catched modulo N
## Basically we can take 17th root of C
## Couldnt find better method to take 17th root so I took until 1.0625th power 
sqrted = v.sqrt().sqrt().sqrt().sqrt()

sqrted = int(sqrted)

res = int(pow(sqrted, (1/1.0625)))
print(res)
length = res.bit_length()
# 288
print(length)




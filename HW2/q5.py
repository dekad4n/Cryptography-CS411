import lfsr 
import random

length = 256
## SEEDS DOESNT MATTER --> THE IMPORTANCE IS IN PERIOD!
########################## A 
print("LFSR: **************")
L = 6
C = [0]*(L+1)
S = [0]*L
# INITIALIZE 
C[0] = C[1] = C[4] = C[5] =  C[6] = 1  

for i in range(0, L):            # for random initial state
    S[i] = random.randint(0, 1)
print("Initial state: ", S)

keystream = [0]*length
for i in range(0, length):
    keystream[i] = lfsr.LFSR(C, S)

print("First period: ", lfsr.FindPeriod(keystream))

########################## B
print("LFSR: **************")
L = 6
C = [0]*(L+1)
S = [0]*L

C[0] = C[2] = C[6] = 1  

for i in range(0, L):            # for random initial state
    S[i] = random.randint(0, 1)
print("Initial state: ", S)
# Find keystream
keystream = [0]*length
for i in range(0, length):
    keystream[i] = lfsr.LFSR(C, S)
# Find period
print("First period: ", lfsr.FindPeriod(keystream))

########################## C
print("LFSR: **************")
L = 5
C = [0]*(L+1)
S = [0]*L

C[0] = C[3] = C[5] = 1

for i in range(0, L):            # for random initial state
    S[i] = random.randint(0, 1)
print("Initial state: ", S)

keystream = [0]*length
for i in range(0, length):
    keystream[i] = lfsr.LFSR(C, S)

print("First period: ", lfsr.FindPeriod(keystream))


print('A generates maximum period since period is equals to 2^6 - 1 (63)')
print('B does not generate maximum period since period is not equal to 2^6 - 1 (14)')
print('C generates maximum period since period is equals to 2^5 - 1 (31)')
## YES
## NO
## YES
import RSA_Oracle_client as rsa
import random as rn

# Converts integer to bytes array
def intToBytes(pr):
    ln = pr.bit_length()
    bytelen = (ln + 7) // 8
    return pr.to_bytes(bytelen, byteorder="big")

# get values
c , n , e = rsa.RSA_Oracle_Get()
# create a random integer (the value does not matter)
rn = rn.randint(0,1000)
# q = c * (r ** e mod(n)) mod(n) = c*(r**e) mod(n)
queryPar =  (c * pow(rn,e,n)) %n

# get m_ = C**d * (r**(ed) mod N) mod N  = m**ed * r**ed mod(N) = m * r mod(N)
ans = rsa.RSA_Oracle_Query(queryPar)
# ans = m * r
# res = r**-1 * ans
res = (rsa.modinv(rn, n) * ans) % n
# convert int value to bytes
res = intToBytes(res).decode()

print(res)
rsa.RSA_Oracle_Checker(res)
import client
import galois as gls

poly = client.get_poly()

a,b = poly[0], poly[1]

irred = gls.Poly.Str("x^8 + x^4 + x^3 + x + 1")
GF = gls.GF(2**8, irreducible_poly=irred)
# a_arr = [int(c) for c in a]
# b_arr = [int(c) for c in b]
a_arr = int(a, 2)
b_arr = int(b, 2)
gls_a = GF(a_arr)
gls_b = GF(b_arr)

res = gls_a * gls_b
# print(res)
print("---- PART A ----")
res = int(res)
stres = "" 
for i in range(7,-1, -1):
    if(2**i <= res):
        res -= 2**i
        stres += "1"
    else:
        stres += "0"
print(stres, int(stres, 2))
client.check_mult(stres)

## Q2
full = int("00000001",2)
gls_f = GF(full)

res = (gls_f/gls_a)

res = int(res)
print("---- PART B ----")
print(res, end=" ")
stres = ""
for i in range(7, -1, -1):
    if(2**i <= res):
        res -= 2**i
        stres += "1"
    else:
        stres += "0"
print(stres)
client.check_inv(stres)

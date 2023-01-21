# %%
#include all libraries

import Client
from ecpy.curves import Curve, Point
from Crypto.Hash import SHA3_256,HMAC, SHA256
from Crypto import Random   # a bit better secure random number generation 
import hashlib
import random

# %%
RESET = True
RCODE = 970900
stuID = 27047
print("IKey is a long term key and shouldn't be changed and private part should be kept secret. But this is a sample run, so here is my private IKey: ")
print("My ID number is", stuID)
Client.stuID = stuID

# %%
#init curve
E = Curve.get_curve('secp256k1')
n = E.order
p = E.field
P = E.generator
a = E.a
b = E.b

IKey_Ser = Point(0xce1a69ecc226f9e667856ce37a44e50dbea3d58e3558078baee8fe5e017a556d, 0x13ddaf97158206b1d80258d7f6a6880e7aaf13180e060bb1e94174e419a4a093,E)


# %%
class KeyPair:
    def __init__(self, prv=None, pub=None):
        self.prv = prv
        self.pub = pub

# %%
def concat_ints(a,b):
    binr = bin(a)[2:]
    binm = bin(b)[2:]

    while len(binm) % 8 != 0:
        binm = '0' + binm

    concat = binr + binm
    concat = int(concat,2)

    byteconcat = concat.to_bytes((concat.bit_length()+7)//8 ,byteorder='big')

    return byteconcat,concat

def generateKey():
    s = random.randint(1, n-1)
    Q = s*P
    return s,Q

def generate_signature(m, sA):
    # 1. k ←Zn, (i.e., k is a random integer in [1, n −2]).
    k = random.randint(1, n - 2)

    # 2. R = k ·P
    R = k * P

    # 3. r = R.x (mod n), where R.x is the x coordinate of R
    r = R.x % n

    # 4. h = SHA3 256(r||m) (mod n)
    byteconcat,concat = concat_ints(r,m)

    h = hashlib.sha3_256(byteconcat)
    h = int(h.hexdigest(), 16) % n

    # 5. s = (k + sA ·h) (mod n)
    s = (k + sA * h) % n

    # 6. The signature for m is the tuple (h, s).
    return (h, s)

def verify_signature(m,h,s,Q):
    V = s*P - h*Q
    v = V.x % n
    hd = SHA3_256.new(concat_ints(v,m)[0])
    hd = int.from_bytes(hd.digest(), byteorder='big') % n
    return hd == h

# %%
# Create and register IKey


if RESET == True:
    Client.ResetIK(RCODE)
IKey = KeyPair(*generateKey())
print("IKEY priv:")
print(IKey.prv)
h, s = generate_signature(stuID, IKey.prv)
print("Signature of my ID number is:")
print("h=", h)
print("s=", s)
if not verify_signature(stuID,h,s,IKey.pub):
    print('Signature verification failed for self-created IKey')
print("Sending signature and my IKEY to server via IKRegReq() function in json format")
Client.IKRegReq(h,s,IKey.pub.x, IKey.pub.y)

print("Received the verification code through email")
CODE = int(input("Enter verification code which is sent to you: "))

print("Sending the verification code to server via IKRegVerify() function in json format")
Client.IKRegVerify(CODE)

# %%
#Create and register SPK
if RESET == True:
    print("SPK reset status:",
    Client.ResetSPK(*generate_signature(stuID,IKey.prv))
    )
print("Generating SPK...")
SPK = KeyPair(*generateKey())
print("Private SPK:",SPK.prv)
print("Public SPK.x:",SPK.pub.x)
print("Public SPK.y:",SPK.pub.y)
cbytes,cint = concat_ints(SPK.pub.x,SPK.pub.y)
print("Signature of SPK is:")
h,s = generate_signature(
    concat_ints(SPK.pub.x,SPK.pub.y)[1],
    IKey.prv)
print("h=",h)
print("s=",s)
print("Sending SPK and the signatures to the server via SPKReg() function in json format...")
xx,yy,hs,ss = Client.SPKReg(h,s,SPK.pub.x, SPK.pub.y)
SPK_s = KeyPair(pub=Point(xx,yy,E))

print("Verifying the server's SPK...")
print("Is SPK verified?:",verify_signature(concat_ints(SPK_s.pub.x,SPK_s.pub.y)[1]
    ,hs,ss,IKey_Ser))

# # %%
# Generation of HMAK Key
print("Creating HMAC key (Diffie Hellman)")
T = SPK.prv * SPK_s.pub
print("T is ", T)
# U = {b’CuriosityIsTheHMACKeyToCreativity’ ∥T.y ∥T.x}
U = b'CuriosityIsTheHMACKeyToCreativity' + T.y.to_bytes((T.y.bit_length()+7)//8 ,byteorder='big') + T.x.to_bytes((T.x.bit_length()+7)//8 ,byteorder='big')
print("U is ", U)

KHMAC = SHA3_256.new(U)

KHMAC = int(KHMAC.hexdigest(), 16)
byteKHMAC = KHMAC.to_bytes((KHMAC.bit_length()+7)//8, byteorder='big')
print("HMAC key is created ", byteKHMAC)

# %%
# generate 10 OTK Key
if RESET == True:
    Client.ResetOTK(*generate_signature(stuID,IKey.prv))
print("Creating OTKs starting from index 0...")
OTKs = []
HMACs = []
for i in range(10):
    x,y = generateKey()
    OTKs.append(KeyPair(x, y))

    print(str(i) + "th key generated. Private part=", OTKs[i].prv)
    print("Public (x coordinate)=", OTKs[i].pub.x)
    print("Public (y coordinate)=", OTKs[i].pub.y)
    concatted = concat_ints(
        OTKs[i].pub.x, OTKs[i].pub.y)[0]
    print("x and y coordinates of the OTK converted to bytes and concatanated message ", concatted)
    
    hmacValue = HMAC.new(byteKHMAC, concatted, digestmod=SHA256)
    hd = hmacValue.hexdigest()
    print("hmac is calculated and converted with 'hexdigest()': ", hd)
    HMACs.append(hd)

    Client.OTKReg(i, OTKs[i].pub.x, OTKs[i].pub.y, HMACs[i])


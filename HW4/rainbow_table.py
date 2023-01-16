# Do not forget to install pycryptodome if not already installed
# pip install pycryptodome

import random
from Crypto.Hash import SHA3_256
from Crypto import Random
import json

def Reduction(x, Alphabet, length, i):
  pwd = ""
  t = x+i
  size = len(Alphabet)
  for j in range(0,length):
    pwd += Alphabet[t%size]
    t = t >> 5
  return pwd

Alphabet = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}
alpha_len = len(Alphabet)
pwd_len = 6
pwd_space = alpha_len**pwd_len 
t = 2**16+1
m = 2*(pwd_space//t)


# Example for computing one link in the chain; i.e., pwd(i+1) = R(H(pwd(i)))
i=0 #ith password
pwd_i = "UTKUAY"
hash = SHA3_256.new(pwd_i.encode('utf-8')) # hash it
digest = int.from_bytes(hash.digest(), byteorder='big') # convert the hash into an integer
pwd_i1 = Reduction(digest%pwd_space, Alphabet, pwd_len, i) # Reduce it
# Read the rainbow table
with open("rainbowtable.txt","r") as f:
    Rainbow_Table = [i.strip("\n").split(" ") for i in f]


# Digests
digest = [0] * 10
digest[0] = 68129488042014195110038312742631656560169409657135532041458285223411948948866 
digest[1] = 46239392724540305843773223468371007649789714008888724404577522963606526935663
digest[2] = 110406129499448663314892102624048071751195087034833389280698385840405018797245
digest[3] = 65313482800699121689791056564159588572328243104099706346813528273728803821799
digest[4] = 26488608998776111812821955234078050783380240707584374240367068144139270378566
digest[5] = 87733593915723119912876120695727808623311037020587654316551147774042989670919
digest[6] = 16344842234414968973159367286253689000345294679806407070533658658954772132386
digest[7] = 11069735230566290933060635309207163848287223244609233713537878009248132037840
digest[8] = 20733450778515206264852019437941451511769124738113724518661416850129619314254
digest[9] = 106933681333642373745676425544794836262079892073184965405213516175561492091091

# Solution
column1 = []
for i in Rainbow_Table:
  column1.append(i[1])
for d in digest:
    w = 0
    found = 0
    while not found:
        password = Reduction(
            d % pwd_space, Alphabet, pwd_len, w)  # reduce it
        d = int.from_bytes(SHA3_256.new(
            password.encode()).digest(), byteorder="big")   # get integer

        if password in column1:  # we found our password at the last column
            idx = column1.index(password)  # find index
            password = Rainbow_Table[idx][0]  # find hashed value
            i = 0
            f2 = 0
            while not f2:  # until password is found
                hash = SHA3_256.new(password.encode())  # hash password
                if password == d:  # found
                    print(password)
                    f2 = 1
                else:
                    # make it integer
                    d = int.from_bytes(hash.digest(), byteorder='big')
                    password = Reduction(
                        d % pwd_space, Alphabet, pwd_len, i)  # not found reduce it again
                    i += 1
            found = 1

        else:
            w += 1

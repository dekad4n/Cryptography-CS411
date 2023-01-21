#%%
import math
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256, HMAC, SHA256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json

API_URL = 'http://10.92.52.255:5000/'

stuID = 26471
stuIDB = 2014

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def Setup():
    E = Curve.get_curve('secp256k1')
    return E


E = Setup()
curve  = E

def KeyGen(E):
    n = E.order
    P = E.generator
    sA = randint(1,n-1)
    QA = sA*P
    return sA, QA

def SignGen(message, E, sA):
    n = E.order
    P = E.generator
    k = randint(1, n-2)
    R = k*P
    r = R.x % n
    h = int.from_bytes(SHA3_256.new(r.to_bytes((r.bit_length()+7)//8, byteorder='big')+message).digest(), byteorder='big')%n
    s = (sA*h + k) % n
    return h, s

def SignVer(message, h, s, E, QA):
    n = E.order
    P = E.generator
    V = s*P - h*QA
    v = V.x % n
    h_ = int.from_bytes(SHA3_256.new(v.to_bytes((v.bit_length()+7)//8, byteorder='big')+message).digest(), byteorder='big')%n
    if h_ == h:
        return True
    else:
        return False


#server's Identitiy public key
IKey_Ser = Point(93223115898197558905062012489877327981787036929201444813217704012422483432813 , 8985629203225767185464920094198364255740987346743912071843303975587695337619, curve)

def IKRegReq(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    if((response.ok) == False): print(response.json())

def IKRegVerify(code):
    mes = {'ID':stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    print(response.json())

def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)		
    if((response.ok) == False): 
        print(response.json())
    else: 
        res = response.json()
        return res['SPKPUB.X'], res['SPKPUB.Y'], res['H'], res['S']

def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True


def ResetIK(rcode):
    mes = {'ID':stuID, 'RCODE': rcode}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetSPK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetOTK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json = mes)		
    print(response.json())

############## The new functions of phase 2 ###############

#Pseudo-client will send you 5 messages to your inbox via server when you call this function
def PseudoSendMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsg"), json = mes)		
    print(response.json())

#Get your messages. server will send 1 message from your inbox
def ReqMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)	
    print(response.json())	
    if((response.ok) == True): 
        res = response.json()
        return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["EK.X"], res["EK.Y"]

#Get the list of the deleted messages' ids.
def ReqDelMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqDelMsgs"), json = mes)      
    print(response.json())      
    if((response.ok) == True): 
        res = response.json()
        return res["MSGID"]

#If you decrypted the message, send back the plaintext for checking
def Checker(stuID, stuIDB, msgID, decmsg):
    mes = {'IDA':stuID, 'IDB':stuIDB, 'MSGID': msgID, 'DECMSG': decmsg}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "Checker"), json = mes)		
    print(response.json())

#%%


import math
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve, Point
from Crypto.Hash import SHA3_256, HMAC, SHA256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json

# These keys are the keys from Phase-1 of the project. 
#   Since this is only phase-2 did not want to regenerate them every time I run the code.
#   Hence, I have hardcoded them here.
KEYS = {"IKey": {"prv": 70028801530215821086009396701460071578064705384059091134930487891625262845363, "pub": {"x": 97701060971149935155738482932525768711096058029429375991336689438824469181326, "y": 1210084207238814845293629025011125714851168420848384926208369217787973574039}}, "SPK": {"prv": 106521280772394825292119554525791285086051566497129671344634427395240349826828, "pub": {"x": 53711874947551167976859579457288009650912679708693714201201776001899673059187, "y": 101709848946951772852672798381069003759071066058681572982654947202532713650250}}, "SPK_s": {"pub": {"x": 85040781858568445399879179922879835942032506645887434621361669108644661638219, "y": 46354559534391251764410704735456214670494836161052287022185178295305851364841}}, "KHMAC": 70372259361935073067984443718096663125107765978165508121461785261720199412802, "OTKs": [{"prv": 3133000977318903855681276542822635961459211059615214829588557589249326097011, "pub": {"x": 63111252302652203197891224356181375773328025757662463096708534534916850420099, "y": 84861091572254654320156879717210902573487244862965444694990325580057620364361}}, {"prv": 39619072816283856004464418251567564044415668158153227368375879227293379987415, "pub": {"x": 36610963733032319467689540711958676673779664394294506796697938312864624261403, "y": 75327717843148245506780991207141271718803276709990503706805520563576274395626}}, {"prv": 115437136225914835086388220440249460586056850844136240589100025580765512375506, "pub": {"x": 4334197448054064559058083605306513194734194428137075438422595085600796111754, "y": 3365485178617921196727779398598390993442631390873954731567183584923988727392}}, {"prv": 12863307669141583171093933597034563088702920493946988125493046232391856540186, "pub": {"x": 78487774566425310320801544295292387145784228798816526898497948729295832752728, "y": 57199204106264914610119103655928824269112885146448588456921828739067869932897}}, {"prv": 48218613147129953932896999644298518788289440774208131544533944720150545959032, "pub": {"x": 35775494086794986304790345659280665548595809458998340546927990058382048437958, "y": 71124478910600640006240539576675873555105910245398181484219257479316077646219}}, {"prv": 30927876002057455960059487999416622405719521828528218252751941898587367442775, "pub": {"x": 38857656446567787842282087105589834557163195972470505249328370335279397747175, "y": 36773730039130597286993429630625111033463349835103201215637095230709953667211}}, {"prv": 44684461901871126690732004048313682631386275253335159779819514267153619442308, "pub": {"x": 57792793083864875075056534713173338660919201048587979365566510235584253589163, "y": 69124220455973105853311517733504268710733382673140283987579642507262434886151}}, {"prv": 24492162298447677600269711182457895748655736913799487036711888144430203896672, "pub": {"x": 17008349863970297580621689299922129477382064886432472238368840115784577362775, "y": 13922954227379776458740721072743555635147889525235333323207048919462733833856}}, {"prv": 4107476743764846182647506100146189523047122294662635081306748294501014271309, "pub": {"x": 50737931424131468503389222584296090807738697352778428438916533566730013985746, "y": 94728241664923673789286903971616559225403220917732539460795453337609119389838}}, {"prv": 46023880202946454873999278873740599139761751864911792430461608994723280659315, "pub": {"x": 3162001754271329648931665167410105955231166012578396936436049422776347437202, "y": 40859805636295342870948603557411003634720340023657282362444058325088823514596}}]}


E = Setup()
curve  = E

def intToBytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def concat_ints(a, b):
    binr = bin(a)[2:]
    binm = bin(b)[2:]

    while len(binm) % 8 != 0:
        binm = '0' + binm

    concat = binr + binm
    concat = int(concat, 2)

    byteconcat = concat.to_bytes((concat.bit_length()+7)//8, byteorder='big')

    return byteconcat, concat


def generateSessionKey(otk, ek):
    T = otk * ek
    byteconcat, concat = concat_ints(T.x, T.y)
    U = byteconcat + b"ToBeOrNotToBe"
    ks = SHA3_256.new(U)
    return ks.digest()


def chain(ks):
    kenc = SHA3_256.new(ks + b"YouTalkingToMe").digest()
    KHMAC = SHA3_256.new(ks + kenc + b"YouCannotHandleTheTruth").digest()
    kdfnext = SHA3_256.new(kenc + KHMAC + b"MayTheForceBeWithYou").digest()
    return kenc, KHMAC, kdfnext


print("Checking the inbox for incoming messages")
print("Signing my stuID with my private IK")
# PseudoSendMsg
h, s = SignGen(intToBytes(stuID), E, KEYS['IKey']['prv'])
PseudoSendMsg(h, s)


messages = []
for i in range(5):
    try:
        IDB, OTKID, MSGID, MSG, EKx, EKy = ReqMsg(h, s)
    except TypeError:
        quit()
    print("I got this from client", str(stuIDB) + ":")
    print(MSG)
    ek = Point(EKx, EKy, E)
    ks = generateSessionKey(KEYS['OTKs'][OTKID]['prv'], ek)

    

    print("Converting message to bytes to decrypt it...")
    # MSG to byte array
    MSG = MSG.to_bytes((MSG.bit_length() + 7) // 8, 'big')
    print("Converted message is:")
    print(MSG)

    print("Generating the key Ks, Kenc, & Khmac and then the HMAC value ..")
    for i in range(MSGID):
        kenc, KHMAC, ks = chain(ks)
    print("hmac is: ", KHMAC)

    # MSG = nonce || ciphertext || MAC
    # nonce = 8 bytes
    nonce = MSG[:8]
    message = MSG[8:-32]
    mac = MSG[-32:]

    cipher = AES.new(kenc, AES.MODE_CTR, nonce=nonce)

    # Decrypt the message
    plaintext = cipher.decrypt(message).decode()
    print(plaintext)

    # verify the plaintext with the MAC
    hmac = HMAC.new(KHMAC, digestmod=SHA256)
    hmac.update(message)

    if hmac.digest() == mac:
        print("Hmac value is verified")
        print("The collected plaintext: ",plaintext)
        Checker(stuID, IDB, MSGID, plaintext)
        messages.append((i+1, plaintext))
    else:
        print("Hmac value couldn't be verified")
        Checker(stuID, IDB, MSGID, "INVALIDHMAC")

deleted = ReqDelMsg(h, s)
for msg in messages:
    if msg[0] in deleted:
        print("Message {} - Was deleted by sender - X".format(msg[0]))
    else:
        print(f"Message {msg[0]} -", msg[1], "- Read")

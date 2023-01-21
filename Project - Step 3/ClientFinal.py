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
import os
from os.path import exists


API_URL = 'http://10.92.52.255:5000/'

stuID = 26471
stuIDB = 18007

OTKs = []

def Setup():
	global E
	E = Curve.get_curve('secp256k1')
	return E

curve = Setup()
E = Setup()
n = E.order
p = E.field
P = E.generator
a = E.a
b = E.b

IKey_Ser = Point(93223115898197558905062012489877327981787036929201444813217704012422483432813 , 8985629203225767185464920094198364255740987346743912071843303975587695337619, curve)

# classes
class KeyPair:
	def __init__(self, prv=None, pub=None):
		self.prv = prv
		self.pub = pub


# functions

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


def KeyGen(E):
	n = E.order
	P = E.generator
	sA = randint(1,n-1)
	QA = sA*P
	return sA, QA

def SignGen(message, E, sA):
	if type(message) == int:
		message = message.to_bytes((message.bit_length()+7)//8, byteorder='big')
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

def IKRegReq(h,s,x,y):
	mes = {'ID': stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
	if((response.ok) == False): print(response.json())

def IKRegVerify(code):
	mes = {'ID': stuID, 'CODE': code}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
	if((response.ok) == False): raise Exception(response.json())
	print(response.json())

def SPKReg(h,s,x,y):
	mes = {'ID': stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)		
	if(response.ok == False):
		print(response.json())
	else: 
		res = response.json()
		return res['SPKPUB.X'], res['SPKPUB.Y'], res['H'], res['S']

def OTKReg(keyID,x,y,hmac, showmsgs = True):
	mes = {'ID': stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
	if showmsgs:
		print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)
	if showmsgs:	
		print(response.json())
	if((response.ok) == False): return False
	else: return True


def ResetIK(rcode):
	mes = {'ID': stuID, 'RCODE': rcode}
	print("Sending message is: ", mes)
	response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
	print(response.json())
	if((response.ok) == False): return False
	else: return True

def ResetSPK(h,s):
	mes = {'ID': stuID, 'H': h, 'S': s}
	print("Sending message is: ", mes)
	response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
	print(response.json())
	if((response.ok) == False): return False
	else: return True

def PseudoSendMsgPH3(h,s):
	mes = {'ID': stuID, 'H': h, 'S': s}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsgPH3"), json=mes)
	print(response.json())

def ReqMsg(h,s):
	mes = {'ID': stuID, 'H': h, 'S': s}
	print("Sending message is: ", mes)
	response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json=mes)
	print(response.json())	
	if((response.ok) == True): 
		res = response.json()
		return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["EK.X"], res["EK.Y"]

def ReqDelMsg(h,s):
	mes = {'ID':stuID, 'H': h, 'S': s}
	print("Sending message is: ", mes)
	response = requests.get('{}/{}'.format(API_URL, "ReqDelMsgs"), json = mes)
	print(response.json())
	if((response.ok) == True):
		res = response.json()
		return res["MSGID"]

def Checker(stuID, stuIDB, msgID, decmsg):
	mes = {'IDA': stuID, 'IDB':stuIDB, 'MSGID': msgID, 'DECMSG': decmsg}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "Checker"), json=mes)
	print(response.json())
	
	
def SendMsg(idA, idB, otkID, msgid, msg, ekx, eky):
	mes = {"IDA": idA, "IDB": idB, "OTKID": int(otkID), "MSGID": msgid, "MSG": msg, "EK.X": ekx, "EK.Y": eky}
	print("Sending message is: ", mes)
	response = requests.put('{}/{}'.format(API_URL, "SendMSG"), json=mes)
	print(response.json())	
		
def reqOTKB(stuID, stuIDB, h, s):
	OTK_request_msg = {'IDA': stuID, 'IDB':stuIDB, 'S': s, 'H': h}
	print("Requesting party B's OTK ...")
	response = requests.get('{}/{}'.format(API_URL, "ReqOTK"), json=OTK_request_msg)
	print(response.json()) 
	if((response.ok) == True):
		print(response.json()) 
		res = response.json()
		return res['KEYID'], res['OTK.X'], res['OTK.Y']
		
	else:
		return -1, 0, 0

def Status(stuID, h, s, showMsgs = True):
	mes = {'ID': stuID, 'H': h, 'S': s}
	if showMsgs:
		print("Sending message is: ", mes)
	response = requests.get('{}/{}'.format(API_URL, "Status"), json=mes)
	if showMsgs:
		print(response.json())
	if (response.ok == True):
		res = response.json()
		return res['numMSG'], res['numOTK'], res['StatusMSG']



# Our functions
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


def encrypt(plaintext, kenc, KHMAC):
    nonce_num = randint(2**63, 2**64-1)
    nonce = nonce_num.to_bytes((nonce_num.bit_length()+7)//8, byteorder='big')
    message = bytes(plaintext, "utf-8")
    
    cipher = AES.new(kenc, AES.MODE_CTR, nonce=nonce)
    encrypted = cipher.encrypt(message)
    hmac = HMAC.new(KHMAC, msg=encrypted, digestmod=SHA256)
    hmac_digest_int = int.from_bytes(hmac.digest(), 'big') % n
    hmac_digest_bytes = hmac_digest_int.to_bytes(
    	(hmac_digest_int.bit_length() + 7) // 8, byteorder='big')
    return int.from_bytes(nonce + encrypted + hmac_digest_bytes, byteorder='big')



def decrypt(MSG, kenc, KHMAC):
	if type(MSG) == int:
		MSG = MSG.to_bytes((MSG.bit_length()+7)//8, byteorder='big')
	nonce = MSG[:8]
	message = MSG[8:-32]
	mac = MSG[-32:]
	
	cipher = AES.new(kenc, AES.MODE_CTR, nonce=nonce)

	# Decrypt the message
	plaintext = cipher.decrypt(message).decode()

	# verify the plaintext with the MAC
	hmac = HMAC.new(KHMAC, digestmod=SHA256)
	hmac.update(message)

	return hmac.digest() == mac, plaintext

def generateKey():
	global curve
	s = random.randint(1, (curve.order)-1)
	Q = s*(curve.generator)
	return s,Q


### phase 1
RESET = True

def IKgenerate(key = None):
	global IKey, E

	if key != None:
		IKey = KeyPair(key['prv'], Point(key['pub.x'], key['pub.y'],E))
		return IKey

	IKey = KeyPair(*generateKey())
	if RESET == True:
		RCODE = int(input("Enter the reset code: "))
		ResetIK(RCODE)

	IKRegReq(*SignGen(stuID, E, IKey.prv)
		,IKey.pub.x, IKey.pub.y)

	CODE = int(input("Enter the verification code: "))
	IKRegVerify(CODE)

	return IKey


def SPKgenerate(key=None, spks=None):
	global SPK, E, SPK_s

	if key != None:
		SPK = KeyPair(key['prv'], Point(key['pub.x'], key['pub.y'], E))
		SPK_s = KeyPair(pub=Point(spks['pub.x'], spks['pub.y'], E))
		return SPK
	SPK = KeyPair(*generateKey())
	print(SPK.prv)

	if RESET == True:
		ResetSPK(*SignGen(stuID, E, IKey.prv))

	h, s = SignGen(concat_ints(SPK.pub.x, SPK.pub.y)[1], E, IKey.prv)

	xx, yy, hs, ss = SPKReg(h, s, SPK.pub.x, SPK.pub.y)
	SPK_s = KeyPair(pub=Point(xx, yy, E))
	print(xx, yy, "server")
	server_verified = SignVer(concat_ints(
		SPK_s.pub.x, SPK_s.pub.y)[0], hs, ss, E, IKey_Ser)
	
	if server_verified:
		print("Server verified SPK")
		return SPK
	else:
		print("Server did not verify SPK")

def generateOTK(showmsgs = True):
	global KEYS, OTKs, KHMAC, SPK, SPK_s, IKey
	
	numMsg, numOtk, statusMsg = Status(stuID, *SignGen(stuID, E, IKey.prv))
	print(numOtk, "NUM NUM NUM")
	gen = 0
	if numOtk < 10:
		gen = 10 - numOtk
	

	T = SPK.prv * SPK_s.pub
	U = b'CuriosityIsTheHMACKeyToCreativity' + T.y.to_bytes((T.y.bit_length()+7)//8 ,byteorder='big') + T.x.to_bytes((T.x.bit_length()+7)//8 ,byteorder='big')

	KHMAC = SHA3_256.new(U)
	KHMAC = int(KHMAC.hexdigest(), 16)

	byteKHMAC = KHMAC.to_bytes((KHMAC.bit_length()+7)//8, byteorder='big')
	if showmsgs:
		print("HMAC key is created ", byteKHMAC)
	if showmsgs:
		print("Creating OTKs starting from index 0...")
	lastOTKId = 0
	if exists('./OTKs.json'):
		with open('OTKs.json', 'r') as f:
			jOTKs = json.loads(f.read())
			lastOTKId = jOTKs["lastOTKId"]
	HMACs = []
	for i in range(gen):
		prv,pub = KeyGen(E)
		OTKs.append({"KeyPair": KeyPair(prv,pub), "OTKId": i + 1 +lastOTKId})
		if showmsgs:
			print(str(i + lastOTKId) + "th key generated. Private part=", OTKs[len(OTKs)-1]["KeyPair"].prv)
			print("Public (x coordinate)=", OTKs[len(OTKs) -1 ]["KeyPair"].pub.x)
			print("Public (y coordinate)=", OTKs[len(OTKs) -1 ]["KeyPair"].pub.y)
		concatted = concat_ints(
			OTKs[len(OTKs) - 1]["KeyPair"].pub.x, OTKs[len(OTKs) - 1]["KeyPair"].pub.y)[0]
		if showmsgs:
			print("x and y coordinates of the OTK converted to bytes and concatanated message ", concatted)
		
		hmacValue = HMAC.new(byteKHMAC, concatted, digestmod=SHA256)
		hd = hmacValue.hexdigest()
		if showmsgs:
			print("hmac is calculated and converted with 'hexdigest()': ", hd)
		HMACs.append(hd)

		OTKReg(lastOTKId + 1 + i, OTKs[len(OTKs) - 1]["KeyPair"].pub.x,
		       OTKs[len(OTKs) - 1]["KeyPair"].pub.y, HMACs[i], showmsgs)

	# open OTKs file and write OTKs array
	with open('OTKs.json', 'w') as f:
		jOTKs = [{'prv': OTKs[i]["KeyPair"].prv, 'pub.x': OTKs[i]["KeyPair"].pub.x,
           'pub.y': OTKs[i]["KeyPair"].pub.y, "OTKId": OTKs[0]["OTKId"] + i} for i in range(len(OTKs))]
		newJOTKs = {"OTKs": jOTKs, "lastOTKId": jOTKs[len(jOTKs) -1]["OTKId"]}
		newJOTKs = json.dumps(newJOTKs)

		f.write(newJOTKs)
		f.close()
	

def ResetOTK(h,s):
	mes = {'ID': stuID, 'H': h, 'S': s}
	print("Sending message is: ", mes)
	response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json=mes)
	print(response.json())

	# if OTKs.json exists, delete it
	if os.path.exists('OTKs.json'):
		os.remove('OTKs.json')

def recoverOTKs():
	global OTKs
	# if OTKs.json exists, read it
	if os.path.exists('OTKs.json'):
		with open('OTKs.json', 'r') as f:
			jOTKs = json.loads(f.read())
			OTKs = [{"KeyPair":KeyPair(OTK['prv'], Point(OTK['pub.x'], OTK['pub.y'], E)), "OTKId": OTK["OTKId"] } for OTK in jOTKs["OTKs"]]
			f.close()
			return True
	else:
		return False

def getMessagesFromPseudo():
	h, s = SignGen(stuID, E, IKey.prv)
	PseudoSendMsgPH3(h, s)
	
def encryptMessage(plaintext, to, MSGID, OTKx, OTKy, OTKid, EKpriv,EKpub):
    
	global curve, IKey
	h, s = SignGen(to,curve, IKey.prv)
	print("Generating an ephemeral key ")
	
	print("Private part of my EK:", EKpriv)
	print("Generating the KDF chain for the encryption and the MAC value generation")
	print("Generating session key using my EK and my friend's Public OTK for the message with id ", MSGID)
	KS = generateSessionKey(Point(OTKx, OTKy, curve), EKpriv)
	for i in range(MSGID):
        
		Kenc, KHMAC, KS = chain(KS)

	encrypted = encrypt(plaintext, Kenc, KHMAC)
	return encrypted, EKpub, OTKid
	
def decryptMessage(IDB, OTKID, MSGID, MSG, EKx, EKy):
	global curve, OTKs
	crrOTK = 0
	for i in OTKs:
		if i["OTKId"] == OTKID:
			crrOTK = i["KeyPair"]
	OTK = crrOTK
	EK = Point(EKx, EKy, curve)
	KS = generateSessionKey(OTK.prv, EK)
	for i in range(MSGID):
		Kenc, KHMAC, KS = chain(KS)
	return decrypt(MSG, Kenc, KHMAC)


def imaginaryFriend():
    print("Now I want to send messages to my friend. Her id is 18007. Yes she is also imaginary")
    print("Signing The stuIDB of party B with my private IK")
    ho, so = SignGen(18007, E, IKey.prv)
    OTKid, OTKx, OTKy = reqOTKB(stuID, 18007, ho, so)
    if OTKid == -1:
        print("My imaginary friend has no OTK!!!!")
        return
    print("The other party's OTK public key is acquired from the server ...")
    print("Generating Ephemeral key")
    EKpriv, EKpub = KeyGen(curve)
    print("The message I want to send: Dormammu, I have come to bargain")
    encrypted, EKpub, OTKid = encryptMessage(
        "Dormammu, I have come to bargain", 18007, 1,  OTKx, OTKy, OTKid, EKpriv, EKpub)
    SendMsg(stuID, 18007, OTKid, 1,
            encrypted, EKpub.x, EKpub.y)
    print("Sending another message")
    print("The message I want to send: I've come to talk with you again")
    encrypted, EKpub, OTKid = encryptMessage(
        "I've come to talk with you again", 18007, 2,  OTKx, OTKy, OTKid, EKpriv, EKpub)
    SendMsg(stuID, 18007, OTKid, 2,
            encrypted, EKpub.x, EKpub.y)
def Phase3Flow():
    print("Now I'll encrypt the messages I retrieved initially from the server and send it to pseudo-client (26045)")
    print("I'll send them in a single block. But order of the messages should be considered")
    messages = []
    getMessagesFromPseudo()
    print("Signing The stuIDB of party B with my private IK")
    h, s = SignGen(26471, E, IKey.prv)
    ho, so = SignGen(26045, E, IKey.prv)
    OTKid, OTKx, OTKy = reqOTKB(stuID, 26045, ho, so)
    
    print("The other party's OTK public key is acquired from the server ...")
    print("Get the message from the list of received messages ...")

    EKpriv, EKpub = KeyGen(curve)

    for i in range(1, 6):
        IDB, OTKID, MSGID, MSG, EKx, EKy = ReqMsg(h, s)

        valid, decrypted = decryptMessage(
            IDB, OTKID, MSGID, MSG, EKx, EKy)
        if valid:
            print(decrypted)
            messages.append(decrypted)
        else:
            print("Not valid")

    for i in range(1, 6):
        encrypted, EKpub, OTKid = encryptMessage(
            messages[i-1], 26045, i,  OTKx, OTKy, OTKid, EKpriv, EKpub)
        print("Sending the message to the server, so it would deliver it to pseudo-client/user whenever it is active ...")
        SendMsg(stuID, 26045, OTKid, i,
                       encrypted, EKpub.x, EKpub.y)
    print("Checking the status of the inbox...")
    numMsg, numOtk, statusMsg = Status(26471, h, s)

def sendMessageTo(stuIDB, message, id):
	OTKid, OTKx, OTKy = reqOTKB(stuID, stuIDB, *SignGen(stuIDB, E, IKey.prv))
	EKpriv, EKpub = KeyGen(curve)

	encrypted, EKpub, OTKid = encryptMessage(
        message, stuIDB, id,  OTKx, OTKy, OTKid, EKpriv, EKpub)

	SendMsg(stuID, stuIDB, OTKid, id,
                   encrypted, EKpub.x, EKpub.y)

def sendToMyself():
	Status(stuID, *SignGen(stuID, E, IKey.prv))
	sendMessageTo(stuID, "acikTim xD", 31)
	IDB, OTKID, MSGID, MSG, EKx, EKy = ReqMsg(*SignGen(stuID, E, key["prv"]))

	valid, decrypted = decryptMessage(
		IDB, OTKID, MSGID, MSG, EKx, EKy)
	if valid:
		print(decrypted)
	else:
		print("Not valid")

key = {'pub.x': 11156170849693674447642802884200722212132918235730958886121916563948290724645,
       'pub.y': 35093430555419211730167211981685865088616450913978501208475602098823931784710,
       'prv': 24652195662077352112920897675760770035710259516202614564505433833422610638546}

SPK_d = {"pub.x": 32511532919945986898135552352509112997282709056137371244781078247133529776140,
         "pub.y": 8151568843481332685990167642482026262655490412339155485587751794167908325548, "prv": 42943873531820092616360864328036968633608757632327214090483907207890241582552}
SPK_s_d = {"pub.x": 85040781858568445399879179922879835942032506645887434621361669108644661638219,
           "pub.y": 46354559534391251764410704735456214670494836161052287022185178295305851364841}
IKgenerate(key)
SPKgenerate(key=SPK_d, spks=SPK_s_d)
# SPKgenerate()
# ResetOTK(*SignGen(stuID, E, key["prv"]))
recoverOTKs()
generateOTK()

imaginaryFriend()
Phase3Flow()
#sendToMyself()






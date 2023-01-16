
import RSA_OAEP as rsa
import threading
c = 10874572375620617789377153154263475798901864318895755165739361956409713948425
e = 65537
N = 39011863995815647013266848060295512705184137160777355248310252490843225091289
f = open("q2.txt", "w")

def compareEncrpytions(start_pin, end_pin):
    global f, c ,e, N
    start_r,end_r  = 2**7, (2**8 - 1) # the flaw
    # for every random key
    for i in range(start_r, end_r):
        # for every pin value
        for k in range(start_pin, end_pin):
            # encrpty with RSA and check if c is equal to that value
            if c == rsa.RSA_OAEP_Enc(k, e, N , i):
                print("The PIN is:", k)
                f.write(str(k))
                print("The key is:",i)
                break

## Dear TA, if your pc is starving for multithreaded problems, you can use it! 
## But I do not recommend it to use XD 
IS_THERE_THREADS = False
NO_THREADS = 3
if IS_THERE_THREADS:
    x = 10000 // NO_THREADS
    threads = list()
    for i in range(NO_THREADS):
        y = threading.Thread(target=compareEncrpytions, args=(x*i, x*i + x))
        threads.append(y)
        y.start()
else:
    compareEncrpytions(1000,10000)


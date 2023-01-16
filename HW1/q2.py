import hw01_helper
import collections
Q2_VALUE = "ZJOWMJ ZJGC BS UEVRSCC, KSZ ZJSFS GC USZJOV GR GZ."
Q2_VALUE_WITHOUT_SPACE = "ZJOWMJZJGCBSUEVRSCC,KSZZJSFSGCUSZJOVGRGZ."
def find_most_frequent(cipher_text):
    return collections.Counter(Q2_VALUE_WITHOUT_SPACE).most_common(1)[0][0]

def q2_sol():
    # we know T is most frequent letter
    T_VAL = hw01_helper.uppercase["T"]
    most_frequent = find_most_frequent(Q2_VALUE)
    most_frequent_val = hw01_helper.uppercase[most_frequent]
    print(T_VAL, most_frequent_val)

    # Then, 19* alpha + Beta (mod26) = 25
    # alpha can be  [1,27,2] (odd numbers between 1-27)
    class CURR_KEY(object):
        alpha = 0
        beta = 0
        gamma = 0
        theta = 0
    for i in range(1, 26, 1):
        MOD_A_MULT = (T_VAL*i) % 26 # T_VAL * alpha
        CURRENT_BETA = most_frequent_val - MOD_A_MULT
        
        CURR_KEY.alpha = i
        CURR_KEY.beta = CURRENT_BETA
        # you can compute decryption key from encryption key
        CURR_KEY.gamma = hw01_helper.modinv(CURR_KEY.alpha, 26)
        if CURR_KEY.gamma:
            CURR_KEY.theta = 26-(CURR_KEY.gamma*CURR_KEY.beta) % 26

            res = hw01_helper.Affine_Dec(Q2_VALUE, CURR_KEY)
            print(res, " --> alpha:", CURR_KEY.alpha, "beta:", CURR_KEY.beta )
    



if "__main__" == __name__:
    q2_sol()

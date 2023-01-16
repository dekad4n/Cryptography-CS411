import hw01_helper


Q5_VAL = "ZDZUKEO.AANDOGIJTLNEKEPHZUQDX NDS VLNDJGQLYDVSBU.DER.K.UYT"
uppercaseWithAdditions = dict.copy(hw01_helper.uppercase)
uppercaseWithAdditions['.'] = 26
uppercaseWithAdditions[' '] = 27
inv_uppercase_add = dict.copy(hw01_helper.inv_uppercase)
inv_uppercase_add[26] = '.'
inv_uppercase_add[27] = ' '


def Affine_Dec_Add(ptext, key):
    plen = len(ptext)
    ctext = ''
    for i in range(0, plen,2):
        letter1 = ptext[i]
        letter2 = ptext[i+1]
        if letter1 in uppercaseWithAdditions and letter2 in uppercaseWithAdditions:
            poz = uppercaseWithAdditions[letter1] * 28 + uppercaseWithAdditions[letter2]
            poz = (key.gamma*poz+key.theta) % 784
            ctext += inv_uppercase_add[poz // 28] + inv_uppercase_add[poz %28]
        else:
            ctext += ptext[i]
    return ctext
def find_possible_keys(x, res):
    possible_keys = []
    for alpha in range(1,784):
        if not (alpha % 2 == 0 or alpha % 7 == 0):
            beta = (res - alpha * x) % 784
            possible_keys.append({"alpha": alpha, "beta": beta})
    return (possible_keys)


def q5_sol():
    # We know that plain text is not multiple of 2, then the encryptor added X to the end.
    # We know that plain text ends with .
    # Then for last 2 letters, they correspond to .X
    # First letter OUR_FINDING // 28
    # Second letter OUR_FINDING % 28
    encodedNumber = uppercaseWithAdditions["."] * 28 + uppercaseWithAdditions["X"]
    decodedNumber = uppercaseWithAdditions[Q5_VAL[-2]] * \
        28 + uppercaseWithAdditions[Q5_VAL[-1]]
    # 751 * alpha + b (mod 784) = 691 is only equation we have
    possible_keys  = find_possible_keys(encodedNumber, decodedNumber)
    # Time of brute force attack
    class CURR_KEY(object):
        alpha = 0
        beta = 0
        gamma = 0
        theta = 0
    with open('output_q5.txt', 'w') as f:
        for keys in possible_keys:
            CURR_KEY.alpha = keys["alpha"]
            CURR_KEY.beta = keys["beta"]
            CURR_KEY.gamma = hw01_helper.modinv(CURR_KEY.alpha, 784)
            CURR_KEY.theta = 784-(CURR_KEY.gamma*CURR_KEY.beta) % 784
            f.write(Affine_Dec_Add(Q5_VAL, CURR_KEY) + " alpha: " +
                    str(CURR_KEY.alpha) + " beta: " + str(CURR_KEY.beta) + "\n")

    print("Look output_q5.txt !!!!!!")




if __name__ == "__main__":
    q5_sol()
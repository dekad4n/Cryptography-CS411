import hw01_helper
def q1_sol():
    cipher_text = "NGZZK"

    # Brute Force Attack
    UPPERCASE_LETTERS = hw01_helper.uppercase
    INV_UPPERCASE = hw01_helper.inv_uppercase
    # Find codes of cipher text
    code_arr = []
    for i in cipher_text:
        code_arr.append(UPPERCASE_LETTERS[i])
    print(code_arr)

    for key in range(0,26):
        newText = ""
        for val in code_arr:
            newText += INV_UPPERCASE[(val + key) % 26]
        
        print(newText, " --> ", key)


if "__main__" == __name__:
    q1_sol()

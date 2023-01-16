import hw01_helper



def q3_sol():
    # We want to find alpha values
    # We know that modulus is 28^2 in this affine (Two letters)
    # Then alpha* x + b (mod 784)
    # We want gcd(alpha, 784) = 1
    # beta can be anything

    total = 783 # Numbers between [1 - 784)
    # Multiples of 7 that is not odd
    cnt = 0
    for i in range(1,784):
        if(i % 7 == 0 and i % 2 == 0 ):
            cnt += 1
    # Odd numbers 
    odd_numbers = 783 // 2 + 1
    # alpha values
    total = total - odd_numbers - cnt
    print("Alpha counts:", total)

    print( 28 * total)
    return 28*total





if __name__  == "__main__":
    print("Key space is:", q3_sol())
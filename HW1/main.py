import q1, q2, q3, q5, q7

if __name__  == "__main__":
    inp = input("Which solution you want to see? (write 1 or 2 or 3 or 5 or 7): ")
    # If you are looking to this code, I am sorry for your eyes
    # I only know in Java, how should I supposed to call a function from a string variable 
     
    if inp in ["1","2","3","5","7"]:
        if inp == "1":
            q1.q1_sol()
        elif inp == "2":
            q2.q2_sol()
        elif inp == "3":
            q3.q3_sol()
        elif inp == "5":
            q5.q5_sol()
        else:
            q7.q7_sol()
            print("For further Q7 explanations, please look at my report.")
        print("Thanks for choosing main.py")
    else:
        print("Invalid, sry")

    
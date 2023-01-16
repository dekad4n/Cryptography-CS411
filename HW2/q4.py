from math import gcd
from myntl import modinv
n = 1593089977489628213419978935847037520292814625191902216371975
a = 1085484459548069946264190994325065981547479490357385174198606
b = 953189746439821656094084356255725844528749341834716784445794

# The function that generates theorem
def solFinder(a,b,n, q):
    crr_gcd = gcd(a,n)
    # if gcd == 1 there is exactly 1 solution
    # if gcd == d there may be solutions
    if crr_gcd != 1:
        # if d does not divide b, no solutions
        # if divides, there are d many solutions
        if  (b % crr_gcd) == 0:
            print("There are solutions for " + q)
            print("Solutions for "+ q + ": ")
            x = []
            # Implementation of theorem 
            d = crr_gcd
            adivd = (a-1) // d + 1
            bdivd = (b-1) // d + 1
            ndivd = (n-1) // d + 1
            adivd_inv = modinv(adivd, ndivd)
            xw = (adivd_inv * bdivd) % ndivd
            for crr in range(0,crr_gcd):
                x.append(xw + (crr * n//d))
            print(x)
        else:
            print("NO SOLUTION EXISTS for " + q)
    else:
        print("There is exactly one solution for " + q)
        print("Solution: ", end="")
        x = (b* modinv(a,n) ) % n
        print(x)


# a
a_n = 1593089977489628213419978935847037520292814625191902216371975
a_a = 1085484459548069946264190994325065981547479490357385174198606
a_b = 953189746439821656094084356255725844528749341834716784445794
solFinder(a_a,a_b, a_n,"a")

# b
b_n = 1604381279648013370121337611949677864830039917668320704906912
b_a = 363513302982222769246854729203529628172715297372073676369299
b_b = 1306899432917281278335140993361301678049317527759257978568241
solFinder(b_a,b_b,b_n,"b")

# c
c_n = 591375382219300240363628802132113226233154663323164696317092
c_a = 1143601365013264416361441429727110867366620091483828932889862
c_b = 368444135753187037947211618249879699701466381631559610698826
solFinder(c_a, c_b , c_n,"c")

# d
d_n = 72223241701063812950018534557861370515090379790101401906496
d_a = 798442746309714903219853299207137826650460450190001016593820
d_b = 263077027284763417836483401088884721142505761791336585685868
solFinder(d_a, d_b, d_n,"d")

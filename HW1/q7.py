import hw01_helper
import re

Q7_VAL = "JR WYDUGQ AR LRG BTFWB’U UECDC YVTF S CYVNE LY JVS QZYWYDCJC, CAD FAC NRGQ KZTRAB MXYVTRAXIYY, YK SH GHC DOXRL DDYQES UWBG GIJLSPT UN SXF FILCSPT DMOX VB TFW RGNVC SXF YULYO QS TFW CGN. TFW GKQE PGYOF SCWWGQ TMG XCERMO PQE HGK BQYLGFQ INIR, SXF GO FAWURLD ZO YNS GF DGERMJ VGFT FAC DEOYV CJBUJVOTF SFGENQ CMDVKQE UADJ GHC VYQEWYQC QE SUWOR GHC TBKP-A-ZJKE SRME DJR LMO WCATCD. RG EEAGSNRD DJYO FIBW DQ FIBW LGGWCWX VUE TSBKBUQ GLLRCRK KPQ MSDDKCLGWN VUE FSJCEDQ LRCG IL JOCYIRQ VQQGCV YPYY GF RKF MGFN. DRTUWOP N GPSXF CIYFY CAD Y UOPGRC-LKDYE NAVGQ HGYR YVTF TYQXS USC UCAAW PQE A FSVH N DMROP GO USVM NBPWKUG, YCL RG RSQSIGQ IR OSVU TPWZKQARAYP. UIQ ZOCIY YJWU UULY VQBSCDI CG HGK CKQEQ. ZO FVD LGD MAOU ORCG TM VY YVTF LRQFE YJWU NNB ZKPQS, YFN YUEL, LY JVS CPMKGEB NSUVOL, GXG NRK KOGZEB DSCOLC LY DEUQZ KINILKD VUE ZGYMF OL LRG GAZDO, JR LSJMJRD YOKA YIIW K HEIEZDGAEB ZYTFE, ZSBGYY KACUVNE LRG CIYFY UGOMD. RG JARURGQ TFW OCFY USVM BF RZO QGHCJ SP SRMFD QS HGE, KPQ FMJ DJR FGJCV GIKW BGNLGROF GHYL RKF WYDU YNS BAPHRRCFD HEOK LRCG OD GDJRR KWX. JR EVHOTVELUOF N MMEOPGAPQ ZCAG MX CJNMC LRCG HC KRQHLB OKNX SM MXEBURZVA. GHC KGGNT ZMBUG TFJYWTH RZO UXIL GP JVS DGBGUEYV SP GILQ LGNDQ, SXF UE NSEURD YFN OBPNWN JVS ZJYPMEB XKER WGLR JVS FSXFXEPURKRF."

def find_ciphers_repeating(ctext):
    JVS = [m.start()   for m in re.finditer('JVS', ctext)]
    JR = [m.start() for m in re.finditer('JR', ctext)]
    CAD = [m.start() for m in re.finditer('CAD', ctext)]
    LRG = [m.start() for m in re.finditer('LRG', ctext)]

    print("JVS: ")
    for i in range(1,9):
        print(i,": ", end="")
        for k in JVS:
            print(k%i, end = " ")
        print()
    print("JR: ")
    for i in range(1, 9):
        print(i, ": ", end="")
        for k in JR:
            print(k % i, end=" ")
        print()
    print("CAD: ")
    for i in range(1, 9):
        print(i, ": ", end="")
        for k in CAD:
            print(k % i, end=" ")
        print()
    print("LRG: ")
    for i in range(1, 9):
        print(i, ": ", end="")
        for k in LRG:
            print(k % i, end=" ")
        print()
def decrypt(text,keys):
    newText = ""
    key = 0
    for ch in text:
        if ch.isalpha():
            newText += hw01_helper.inv_uppercase[(hw01_helper.uppercase[ch] - keys[key])%26 ]
            key = (key + 1) % len(keys)
        else:
            newText += ch

    with open('output_q7.txt', 'w') as f:
        f.write(newText)
    print("Please look at output_q7.txt !!!")


def q7_sol():
    just_alphabet_chars = re.sub("""[^\w]""", "", Q7_VAL)
    find_ciphers_repeating(just_alphabet_chars)
    
    decrypt(Q7_VAL, keys=[2,13,0,24,18,10])
    
if __name__ == "__main__":
    q7_sol()

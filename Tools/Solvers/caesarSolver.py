from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools # type: ignore

#Editable toggles and shit
string = "FRWXT KFKWB VDXGL BMKNL MMATM RHNKC HNKGX RPTLN GXOXG MYNET GWAHI XRHNP BEEGH MFBGW FRWBK XVMGX LLBGP KBMBG ZMHRH NHGRH NKTKK BOTEB GGXPR HKDBT IIKXV BTMXM ATMRH NFTRG XXWTE BMMEX MBFXM HLXMR HNKHP GIETG LBGFH MBHGU NMMAB GZLTK XFHOB GZLHF XPATM YTLMX KMATG BXGOB LTZXW PAXGB YBKLM TIIKH TVAXW FKUTU UTZXP BMAFR IKHIH LTEBY XTKMA TMBGM AXLXW TGZXK HNLMB FXLBM BLGXV XLLTK RMHKX TVMMH XOXGM LPBMA LIXXW BYPXT KXMHA TOXTG RAHIX HYLAT IBGZH NKWXL MBGRP BMAEN VDBMB LGHMM HHETM XMHXF UTKDH GHNKO XGMNK XBNGW XKLMT GWMAT MRHNK LVAXW NEXBL GHMRX MYBGT EBLXW LHVTG BBFIE HKXRH NMHVH GLBWX KFHOB GZYHK PTKWR HNKOB LBMMH PTLAB GZMHG MAXKX TKXIX HIEXA XKXHY VHGLX JNXGV XPAHT KXXTZ XKMHF XXMPB MARHN TGWPA HFBZA MUXIX KLNTW XWURR HNMHC HBGPB MANLB YMAXL TVKBY BVXHY LHFTG RZHHW FXGTG WPHFX GBLGH MMHUX PTLMX WMAXG PXPBE EGXXW MAXBK LNIIH KMRHN ATOXT EKXTW RLAHP GTKXF TKDTU EXLDB EEBGX QIHLB GZBGC NLMBV XTGWI XKLNT WBGZM AXPXT EMARM HPHKD PBMAR HNMHT WWKXL LBMHG RHNKL BWXHY MAXTM ETGMB VAXKX BGMAX NGBMX WLMTM XLPXT KXWXL IXKTM XERBG GXXWH YRHNK TWOHV TVRBY PXTKX MHVHG LHEBW TMXMA XZTBG LPHGB GHNKF HLMNG VBOBE PTKPB MAFRO XKRUX LMPBL AXLZK XGOBE EXFWH WZX"
ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi"
}
decryptionReady = True

string = string.replace(" ","")
if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"String length: {len(string)}")


def shift(text: str,s: int) -> str:
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result
def recommendedShift(args: dict, mode = "chi")-> int:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])
def recommendedShiftChiSquared(string: str, info = False) -> int:
    minChi = [10**10,0]
    allChis = []
    for i in range(26):
        chi = chiSquared(shift(string,i))

        if chi<minChi[0]:
            minChi = [chi,i]
        allChis.append([chi,i])
    
    if info:
        allChis=sorted(allChis, key=lambda thingy: thingy[0])
        print(allChis[0])
        print(allChis[1])
        print(allChis[2])
    return minChi[1]
def recommendedShiftFrequencyAnalysis(string: str, info = False) -> int:
    frequencies = Counter(string.lower())
    frequenciesVer2 = sorted(list(frequencies.items()), key= lambda thingy: thingy[1], reverse= True)

    maxDetails = ["",0]
    potentialKeys = []
    for letter, freq in frequencies.items():
        if freq>maxDetails[1]:
            maxDetails = [letter.upper(),freq]
            potentialKeys.append([letter.upper(),freq])
    
    distance = ord("E") - ord(maxDetails[0])
    if distance < 0: distance = 26+distance

    if info:
        print(frequenciesVer2[0])
        print(frequenciesVer2[1])
        print(frequenciesVer2[2])
        print(frequenciesVer2[3])

    return distance
def chiSquared(text: str) -> int: #im pretty sure this is a version of standard deviation :sob, adds up the square of each letters occurance subtracted from its expected occurance and divides by expected occurance
    english_letter_frequencies = {
        'E': 0.1270,
        'T': 0.0906,
        'A': 0.0817,
        'O': 0.0751,
        'I': 0.0697,
        'N': 0.0675,
        'S': 0.0633,
        'H': 0.0609,
        'R': 0.0599,
        'D': 0.0425,
        'L': 0.0403,
        'C': 0.0278,
        'U': 0.0276,
        'M': 0.0241,
        'W': 0.0236,
        'F': 0.0223,
        'G': 0.0202,
        'Y': 0.0197,
        'P': 0.0193,
        'B': 0.0149,
        'V': 0.0098,
        'K': 0.0077,
        'J': 0.0015,
        'X': 0.0015,
        'Q': 0.0010, # Note: Often rounded from 0.00095
        'Z': 0.0007
    }
    freqs = Counter(text)
    length = len(text)

    total = 0
    for letter, freq in freqs.items():
        total +=((freq-(english_letter_frequencies[letter.upper()]*length))**2)/english_letter_frequencies[letter.upper()]
    return total
def ic(self):
    freqs = Counter(self)
    length = len(self)

    ioc = sum([value*(value-1) for value in freqs.values()])/(length*(length-1))
    return ioc


if decryptionReady:
    for i,block in enumerate([string]):
        args = {
            "string" : block,
            "info" : True
        }
        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            shiftNum = (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")) or 0
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        if shiftNum:
            string = shift(block,int(shiftNum)).lower()
    if string.islower():
        print(BLUE + string + RESET)
    else:
        print(RED + string + RESET)

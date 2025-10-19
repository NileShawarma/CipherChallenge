from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)

from cipherTools import Affineshift,recommendedShiftChiSquared,inverseText,ic,chiSquared,recommendedShiftFrequencyAnalysis # type: ignore

#FEATURES
"""
CipherText : Auto converted to upper, stripped of punctuation numbers spaces and newlines etc, auto inversed as it is a beaufort cipher

Deciphering: Utilises chi squared to work out probably caesar shift via brute force
Plaintext: Deciphered text is outputted as blue and red for vice versa

Outputs Decryption and encryption keys because idk which ones for what exactly :sob

Toggles: Reversing string, auto deciphering based on key length, auto ic calculator (helps with determining key length)

AutoIC: Prints out the IC's of the first three colummns for a key of size n, loops over all possible key lengths given by AutoICData
"""

#Editable toggles and shit
string = """
DEYRB UGZWR VEFMY PEOAR GTDHX MGWHR RRQRL GSZVE VVIES UZRTU OEHVR SSLLQ VBCYW YHVRL OEUGV TOTGX DVQWU SBLJN HELFQ ARJLL BIIGK JAEGM QGUTG NQAQC ENRYY VOAIK PNJGC YDRPW VFSOV QOTGK KIAWE TPNIC ZKRZI XUSAW NYEUK XEZWA NKIUE OMQHA TZWWR WTSGN IGZGC ZWYFZ HDNHM GZKRZ GINLO EOGJL RUNZD RTGKD RYABL ROMHE AVDAE CIFOY HKDVN FKTUK QFNZA IJEGW MRBSJ NHELF QANKV NRUNG NKOIL KVFHL FKDRT COEGI EKVFG NMJUX LULXJ SZLNZ MEXKP CDGRV IYGNM YOMHK KSHKL OSGTR DGNUU MNKVI NSVBZ YUIHA UQAAP OBHYA SVGFB LOBHZ UNEHE SHGNM ZEUKL VJTTB QSJOO EEKBU KNAEJ MAYNA EJMAY CEIHI VLOEE UZZGE BVKIW MZTJG VGKJT FFSAX BSRZP RATIE LXVSA EQGVQ ZUAUG EAWET EGTNE KRFIW RUYEP EDVGI OEIYF AVNNH QGROK VKIQG LSOEX VRONX XTPAW HRXAV TZHVV IYSAE EIPNV ZEIVE AQDAL CMNXK IEOYP CAHRO AUZGR XDXRF VWYOD RYONK KICWY GNSWA SASVX QVFIE ERQAG TDZKE CHLNG UPNBK AGDWF LVTUK NHRRC FOPRU AIBTQ NSTOK VYEWO OJZPR ECICO JRWSA OUCGA YDZVQ NFALV TOVZZ OKUCG GMIAJ KUGVT VUWRN LNOAB VLCEV ATYSP NJNIG OYIEL XVKBS CKKGZ NETXV NLVRF ICEOU SZWCJ ASLBB MEIUM VKMFF HTHXI YVXOK HGGAC EAKAF VKRYD TFLOE EKERC OLCIM ASSLL AVYUI KKKIF WJRRZ WSZNE ZAXUD LGVUV GNGTC HEIWZ TUKYH KYTZR RBXOO JCMQK GLNLX UEPDN YIAJS AIBEZ ZHSNI TRBKR ZGINO LSUUC YJREK WLRUV LYKKG UXDVD PJAAH GNMZZ NEIXW FAHNZ GNVGI AEEIC JLTGE ZHZNL VVWVX AHREN RKRBV WVNQL DNTLF NKHRV WHYNE FZMQG CAPZI ZANHG SIXKZ HVWLV WCEFL IYRUU KLXVK HCHTV VTMPC DRNFK IGNQA QOCRQ LRDW
"""

ReverseString = False # me when ciphertext was reversed :(
keyLength = 14
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi"
}
decryptionReady = True
AutoICData = {
    "DoAutoIC" : True,
    "StartKey" : 2,
    "MaxKey" : 15
}

string = string.replace(" ","").replace("\n","")
res = ""
for char in string:
    if char.isalpha():
        res+=char
string = res
if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"String length: {len(string)}")

def seperators(string: str,keyLength: int) -> list:
    newArray = ["" for i in range(keyLength)]

    for index in range(keyLength):
        newArray[index] = string[index::keyLength]

    return newArray
def shift(text: str,s: int) -> str:
    return Affineshift(text,[1,s])
def recommendedShift(args: dict, mode = "chi")-> list:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])
string = inverseText(string)
seperatedText = seperators(string,keyLength)
print(string)
if AutoICData["DoAutoIC"]:
    for i in range(AutoICData["StartKey"],AutoICData["MaxKey"]):
        seperatedText = seperators(string,i)
        print(f"Key: {i}")
        seperatedText[0] = shift(seperatedText[0],0).lower()
        seperatedText[1] = shift(seperatedText[1],0).lower()
        seperatedText.append("hi")
        chiSquared(seperatedText[0])
        print(f"IC No1: {round(ic(seperatedText[0]),8)}, IC No2 : {round(ic(seperatedText[1]),8)}, IC No3 : {round(ic(seperatedText[2]),8)}")
decryptionKey = ""
if decryptionReady:
    seperatedText = seperators(string,keyLength)
    for i,block in enumerate(seperatedText):
        args = {
            "string" : block,
            "info" : True
        }
        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            shiftNum = (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")) or 0
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])[1]
        if shiftNum or shiftNum==0:
            seperatedText[i] = shift(block,shiftNum).lower()
            decryptionKey+=str(shiftNum-1)+"|"
        else:
            decryptionKey+="-"+"|"
result = ""
for subkey in decryptionKey.split("|"):
    if subkey!="-" and subkey!="":
        result+=chr(int(subkey)+97)
    else:
        result+="-"
result2 = ""
for subkey in decryptionKey.split("|"):
    if subkey!="-" and subkey!="":
        if subkey=="0": result2+="Z"
        else:result2+=chr((97+26)-int(subkey)).upper()
    else:
        result2+="-"
print(f"\n\n{RED}Decryption key: {result}\nCaesar Equiv: {decryptionKey}\nEncryption Key: {result2}{RESET}")
newString = ""
if decipherData["Ready"]:
    for i in range(len(string)):
        if (i%keyLength)==0: 
            print(newString)
            newString = ""
        character = seperatedText[i%keyLength][i//keyLength]
        if character.isupper():
            newString += RED + character + RESET
        else:
            newString += BLUE + character + RESET
    print(newString)

from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

from cipherTools import Affineshift,recommendedShiftChiSquared,ic,chiSquared,recommendedShiftFrequencyAnalysis # type: ignore

#Editable toggles and shit
string = """
DEYRB UGZWR VEFMY PEOAR GTDHX MGWHR RRQRL GSZVE VVIES UZRTU OEHVR SSLLQ VBCYW YHVRL OEUGV TOTGX DVQWU SBLJN HELFQ ARJLL BIIGK JAEGM QGUTG NQAQC ENRYY VOAIK PNJGC YDRPW VFSOV QOTGK KIAWE TPNIC ZKRZI XUSAW NYEUK XEZWA NKIUE OMQHA TZWWR WTSGN IGZGC ZWYFZ HDNHM GZKRZ GINLO EOGJL RUNZD RTGKD RYABL ROMHE AVDAE CIFOY HKDVN FKTUK QFNZA IJEGW MRBSJ NHELF QANKV NRUNG NKOIL KVFHL FKDRT COEGI EKVFG NMJUX LULXJ SZLNZ MEXKP CDGRV IYGNM YOMHK KSHKL OSGTR DGNUU MNKVI NSVBZ YUIHA UQAAP OBHYA SVGFB LOBHZ UNEHE SHGNM ZEUKL VJTTB QSJOO EEKBU KNAEJ MAYNA EJMAY CEIHI VLOEE UZZGE BVKIW MZTJG VGKJT FFSAX BSRZP RATIE LXVSA EQGVQ ZUAUG EAWET EGTNE KRFIW RUYEP EDVGI OEIYF AVNNH QGROK VKIQG LSOEX VRONX XTPAW HRXAV TZHVV IYSAE EIPNV ZEIVE AQDAL CMNXK IEOYP CAHRO AUZGR XDXRF VWYOD RYONK KICWY GNSWA SASVX QVFIE ERQAG TDZKE CHLNG UPNBK AGDWF LVTUK NHRRC FOPRU AIBTQ NSTOK VYEWO OJZPR ECICO JRWSA OUCGA YDZVQ NFALV TOVZZ OKUCG GMIAJ KUGVT VUWRN LNOAB VLCEV ATYSP NJNIG OYIEL XVKBS CKKGZ NETXV NLVRF ICEOU SZWCJ ASLBB MEIUM VKMFF HTHXI YVXOK HGGAC EAKAF VKRYD TFLOE EKERC OLCIM ASSLL AVYUI KKKIF WJRRZ WSZNE ZAXUD LGVUV GNGTC HEIWZ TUKYH KYTZR RBXOO JCMQK GLNLX UEPDN YIAJS AIBEZ ZHSNI TRBKR ZGINO LSUUC YJREK WLRUV LYKKG UXDVD PJAAH GNMZZ NEIXW FAHNZ GNVGI AEEIC JLTGE ZHZNL VVWVX AHREN RKRBV WVNQL DNTLF NKHRV WHYNE FZMQG CAPZI ZANHG SIXKZ HVWLV WCEFL IYRUU KLXVK HCHTV VTMPC DRNFK IGNQA QOCRQ LRDW
""".upper()
ReverseString = False # me when ciphertext was reversed :(
keyLength = 14
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi",
    "AffineOrCaesar": "Affine" #when this is affine its basically quagmire II
}
decryptionReady = True
AutoICData = {
    "DoAutoIC" : True,
    "StartKey" : 2,
    "MaxKey" : 33
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
def recommendedShift(args: dict, mode = "chi")-> int:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])

seperatedText = seperators(string,keyLength)

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
        typeShift = decipherData["AffineOrCaesar"]
        args = {
            "string" : block,
            "info" : True,
            "CaesarOrAffine": typeShift
        }
        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            if typeShift=="Caesar":
                shiftNum = (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")) 
            else:
                shiftNum = [int(i) for i in (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")).split(",")]
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        if shiftNum or shiftNum==0 or len(shiftNum)>1:
            if typeShift=="Caesar":
                seperatedText[i] = shift(block,int(shiftNum)).lower()
            else:
                seperatedText[i] = Affineshift(block,shiftNum).lower()   
                continue #im not dealing with turning this into a readable key ibr             
            decryptionKey+=str(shiftNum)+"|"
        else:
            decryptionKey+="-"+"|"


#Converts key into words and stuff if its caesar cus i hab no idea how to do it for affine
if typeShift == "Caesar":
    result = ""
    for subkey in decryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            result+=chr(int(subkey)+97)
        else:
            result+="-"
    result2 = ""
    for subkey in decryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            if subkey=="0": result2+="A"
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

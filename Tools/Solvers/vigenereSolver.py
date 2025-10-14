from collections import Counter

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
    "AffineOrCaesar": "Caesar" #when this is affine its basically quagmire II
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

#i love chi squared so fucking much, LIKE DUDE I DONT HAVE TO READ EACH CIPHER TEXT TO CHECK
#wait if i add crib checking with it.... good god
def seperators(string: str,keyLength: int) -> list:
    newArray = ["" for i in range(keyLength)]

    for index in range(keyLength):
        newArray[index] = string[index::keyLength]

    return newArray
def Affineshift(text: str,key: list) -> str:
    result = ""
    multi = key[0]
    shift = key[1]
    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((((ord(char)-65)*multi)+(shift))%26+65)
        # Encrypt lowercase characters
        else:
            result += chr( ( ( (ord(char)-97) *multi) +shift) % 26 + 97)

    return result
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
    possibleMultis = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    if args["CaesarOrAffine"] == "Caesar":
        for i in range(26):
            chi = chiSquared(shift(string,i))

            if chi<minChi[0]:
                minChi = [chi,i]
            allChis.append([chi,i])
    else:
        for j in possibleMultis:
            for i in range(26):
                chi = chiSquared(Affineshift(string,[j,i]))

                if chi<minChi[0]:
                    minChi = [chi,[j,i]]
                allChis.append([chi,[j,i]])
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
        'Q': 0.0010,
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
"""
new = [firstPart,secondPart,thirdPart,fourthPart,fifthPart,sixthPart]
newString = ""
for i in range(len(string)):
    print(i//6)
    try:
        if new[i%6][i//6].isupper():
            newString+="_"
        else: newString+=new[i%6][i//6]
    except: pass
print(newString)
while True:
    pass
"""
from itertools import permutations
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools # type: ignore

string = """
DEYRB UGZWR VEFMY PEOAR GTDHX MGWHR RRQRL GSZVE VVIES UZRTU OEHVR SSLLQ VBCYW YHVRL OEUGV TOTGX DVQWU SBLJN HELFQ ARJLL BIIGK JAEGM QGUTG NQAQC ENRYY VOAIK PNJGC YDRPW VFSOV QOTGK KIAWE TPNIC ZKRZI XUSAW NYEUK XEZWA NKIUE OMQHA TZWWR WTSGN IGZGC ZWYFZ HDNHM GZKRZ GINLO EOGJL RUNZD RTGKD RYABL ROMHE AVDAE CIFOY HKDVN FKTUK QFNZA IJEGW MRBSJ NHELF QANKV NRUNG NKOIL KVFHL FKDRT COEGI EKVFG NMJUX LULXJ SZLNZ MEXKP CDGRV IYGNM YOMHK KSHKL OSGTR DGNUU MNKVI NSVBZ YUIHA UQAAP OBHYA SVGFB LOBHZ UNEHE SHGNM ZEUKL VJTTB QSJOO EEKBU KNAEJ MAYNA EJMAY CEIHI VLOEE UZZGE BVKIW MZTJG VGKJT FFSAX BSRZP RATIE LXVSA EQGVQ ZUAUG EAWET EGTNE KRFIW RUYEP EDVGI OEIYF AVNNH QGROK VKIQG LSOEX VRONX XTPAW HRXAV TZHVV IYSAE EIPNV ZEIVE AQDAL CMNXK IEOYP CAHRO AUZGR XDXRF VWYOD RYONK KICWY GNSWA SASVX QVFIE ERQAG TDZKE CHLNG UPNBK AGDWF LVTUK NHRRC FOPRU AIBTQ NSTOK VYEWO OJZPR ECICO JRWSA OUCGA YDZVQ NFALV TOVZZ OKUCG GMIAJ KUGVT VUWRN LNOAB VLCEV ATYSP NJNIG OYIEL XVKBS CKKGZ NETXV NLVRF ICEOU SZWCJ ASLBB MEIUM VKMFF HTHXI YVXOK HGGAC EAKAF VKRYD TFLOE EKERC OLCIM ASSLL AVYUI KKKIF WJRRZ WSZNE ZAXUD LGVUV GNGTC HEIWZ TUKYH KYTZR RBXOO JCMQK GLNLX UEPDN YIAJS AIBEZ ZHSNI TRBKR ZGINO LSUUC YJREK WLRUV LYKKG UXDVD PJAAH GNMZZ NEIXW FAHNZ GNVGI AEEIC JLTGE ZHZNL VVWVX AHREN RKRBV WVNQL DNTLF NKHRV WHYNE FZMQG CAPZI ZANHG SIXKZ HVWLV WCEFL IYRUU KLXVK HCHTV VTMPC DRNFK IGNQA QOCRQ LRDW
"""
cribs = ["dynamix","citadelle","pds", "syndicate","gravitational", "waves","jamelia","martin","seismological","phenomenon","neutron", "star"]

#Editable toggles and shit
ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi" #how we try to guesstimate the key
}
decryptionReady = True

string = string.replace(" ","")
result = ""

for char in string:
    if char.isalpha():
        result+=char
string = result

if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


string = "".join(string.split(" "))[::1]

print(len(string))
input()

#converts cipher text into nth long chunks which we can acc manipulate, im not sure why i decided to use 2d arrays for this but im not touching this function its too delicate
def chunkBreaker(string: list, length: int, readMode = "row") -> list:
    numChunks = len(string)//length

    match readMode:
        case "row":
            chunks=[]
            for index in range(0,len(string)-length+1,length): #plus one cus arrays 0 based and range doesnt acc hit the max value
                chunks.append([string[index:index+length]])
            return chunks

        case "column":
            chunks = [[""] for j in range(numChunks)]

            for index in range(0,len(string)):
                listNumber = index%(numChunks) 
                chunks[listNumber][0] += string[index]
                        
            return chunks

def swapValues(array: list,key: list) -> list:
    newArray = [None for i in array[0]] #Makes an empty copy of the given ciphered array

    for index,value in enumerate(key):
        newArray[index] = array[0][value] #Each value of the new array is given the nth key value of the ciphered array
    return newArray

def all_full_permutations(lst):#chatgpt'd code here ibr rest is clean
    return [list(p) for p in permutations(lst, len(lst))]

if __name__ == "__main__":
    while True:
        testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
        chunkLength = 5

        chunkified = chunkBreaker(string,chunkLength,"column")
        print(chunkified)

        input(chunkified[-1])
        print(all_full_permutations([i for i in range(chunkLength)]))
        for key in all_full_permutations([i for i in range(chunkLength)]):
            
            decipheredText = ""
            for chunk in chunkified:
                decipheredText += "".join(swapValues(chunk,key))
            print("\n")
            print(decipheredText)
            print("\n")

            for i in cribs:
                if i.upper() in decipheredText:
                    input()
        chunkLength = int(input("End of decryption: "))
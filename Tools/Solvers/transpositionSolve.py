from itertools import permutations
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools # type: ignore

string = """
EAMYD KERRO THSMI GRHOW FYATI TOING RFHEA YOROM ASUIW CECON DTRNE THHAT IRETH NDTEE OFAYS ENSIL INCES OUCEY STRLA SAMES IGGEM AVHTH DIEIN EDCAT TYTHA ADOUH NGCHA OUEDY NDRMI UTABO AROUR GERAN TTMEN OCHED NTUME PRYOU DEOVI EXDIS METRE ROLYP INMIS DMGAN RTYPA SANER EEREK SENTO REEMO YOARE KEULI OBLYT LEEAB BTTOO MOAIN AMRES SIPLE MTFIA NVOCO EOINC RSTHE NVTOI THEST TWENI DBOUL ODEGO ROTOP ETVID WIHEM VITHE CEDEN HEOFT UEVAL HEOFT URIRP SECHA EHSOM HIAVE DTNTE THHAT ARERE HEEOT YSRWA TTTHA COHEY PRULD EDOCE ITBUT KIHIN GHTMI POTBE BLSSI DCEAN AIERT WONLY BEULD TEBET RYRFO FWOUI ULECO GODNE TETIA ETSOM GFHIN RAAVO TOBLE PAALL ESRTI OUOFC DMRSE EPAYB TILOT NONGA RCTHE SEOUR MAAND KEYTA EPSOM UAERS NTSIO MMOCO OOITT ROURP ALPOS YOBUT VEUHA URASS STEDU YOHAT VEUHA EISOM UENFL ONNCE DEHIS IOCIS NDNSA REIAM NGLYI OUONY ELTOH ALPSE DETHE OUALY ITRFA LFHFU NDRIE INMOL ARO
"""
cribs = ["my","dear"]

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

        chunkified = chunkBreaker(string,chunkLength,"row")
        print(chunkified)

        input(chunkified[-1])
        print(all_full_permutations([i for i in range(chunkLength)]))
        for key in all_full_permutations([i for i in range(chunkLength)]):
            
            decipheredText = ""
            for chunk in chunkified:
                decipheredText += "".join(swapValues(chunk,key))
            print("\n")
            #print(decipheredText)
            print("\n")
            if decipheredText[0:6]=="MYDEAR":
                print(decipheredText)
                print(key)
                input()
            
            
            """
            
            for i in cribs:
                if i.upper() in decipheredText:
                    input()
                """
        chunkLength = int(input("End of decryption: "))
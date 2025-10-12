from collections import Counter

#Editable toggles and shit
string = "JGSBOJPPRKXGOEVGEKFCGGHHMTQKDAODHTEUUTCPCWONFAZLJZBXSSWTUGXWSPBQUWZCSXODBEWQXANQCEEKJYUQXLIPQKZZFCGEYJFXSERSOTQUDGQTBRYAOEHJOUSTHKMSMPZGWWOEGHYJTPQWBWFISEELJZBVRATXSCXKJXOEDAWPZANWDZBUDJVNHKXYUSSXSYFYSTOUJAVGBKNPHJYVJHWNVXPNIUYFVYRGBKULBFSFHEVGMGSPSNOEFYHUSFWZZXOVEPTKXAORHJOWONFAZLJZBRBGDPGUSEOZKHEDMJWOWWSDSFSFUSSEYJFXSERSOTQUSNFMFQUWOOCYXLIPIUOJTYSGNJFNCIXAATBIDZFGWIOFFCSESHIPFUZGMJONZZBMSVSUOLHWBWBYRVRWLPMUMJVNWCVJPWSKWUIZCUSFHLDNKAOESZDEPMMFSULDCROFJYUHYJQCOEDADLZCZHMTQCDAPYOPNUPYGKNWSTBIRSOOZKXYPQGRKUFDOPNHVYQVESUTCPSLTNFWMABWHJKLDLDKDSMTNCDAPYPGCLBYRCBVJKSFLWGZFGOFDCMRDAPYWOQWUEWPQUMZGGBLPLQNOSSPLGMMUTCPZDBY"
ReverseString = False # me when ciphertext was reversed :(
keyLength = 6
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi"
}
decryptionReady = True
AutoICData = {
    "DoAutoIC" : False,
    "StartKey" : 2,
    "MaxKey" : 15
}

string = string.replace(" ","")
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
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        if shiftNum:
            seperatedText[i] = shift(block,int(shiftNum)).lower()

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
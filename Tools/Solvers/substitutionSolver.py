from collections import Counter
import string as st
import os 
import sys
import math
import random

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

RED = "\033[91m"
BLUE = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

from cipherTools import chiSquared # type: ignore

class trigram():
    def __init__(self):
        self.trigrams = {}
        self.totalVal = 0

        trigramPath = os.path.join(script_dir,"..","..","Test","Data","trigrams.txt")
        with open(trigramPath, "r") as file:
            for line in file:
                trigramData = line.split(" ")
                self.trigrams[trigramData[0]] = int(trigramData[1])
                self.totalVal += int(trigramData[1])
            
        for key in list(self.trigrams.keys()):
            probability = self.trigrams[key]/self.totalVal
            self.trigrams[key] = math.log10(probability)

        self.baseScore = math.log10(0.01/self.totalVal)
        print(f"{GREEN}Loaded {len(self.trigrams)} trigrams.{RESET}")
        
    def score(self, text):
        
        finalScore = 0

        for index in range(len(text)-3+1):
            trigram = text[index:index+3].upper()
            
            if trigram in self.trigrams:
                finalScore += self.trigrams[trigram]
            else:
                finalScore += self.baseScore
        
        return finalScore

def shuffleKey(currentKey: str) -> str:
    tempKey = list(currentKey)

    index1 = random.randint(0,len(currentKey)-1)
    index2 = random.randint(0,len(currentKey)-1)

    val1 = tempKey[index1]
    val2 = tempKey[index2]

    tempKey[index1],tempKey[index2] = val2, val1

    return "".join(tempKey)
def decrypt(cipherText: str, key: str) -> str:
    plaintext = ""
    ALPHABET = st.ascii_lowercase
    decryption_map = {c: p for p, c in zip(ALPHABET, key)}

    for char in cipherText:
        if char in decryption_map:
            plaintext+= decryption_map[char]
        else:
            plaintext += char
        
    return plaintext

#Editable toggles and shit
string = """
PZ ORFE XERSQDMMR, D PNHK FYVMVXDHR UVE LAFEMRH, AR DH F XVVO PFS, INK LFS IR DEFHLDIMR, FSO KEFQRM ERFMMZ OVRH SVK HNDK ADP. D ERFO ADH MRKKRE KV ZVN TDKA HVPR LVSLRES (KAFSJ ZVN UVE HRSODSX PR F LVYZ), HRRDSX KAFK DK ORPVSHKEFKRH F MVTSRHH DS ADH HYDEKH, INK D LFS FHHNER ZVN KAFK AR DSKRSOH VSMZ KAR IRHK UVE VNE RSORFQVNE. DK KVVJ KAR LVPIDSRO RUUVEKH VU PZHRMU FSO MVEO OREIZ KV LVSQDSLR ADP VU KAR EDXAKSRHH VU VNE YMFS, INK TADMR AR DH UNMMZ LVPPDKKRO KV VNE LFNHR, AR DH SVK RSKDERMZ FK RFHR TDKA VNE PRKAVOH. D AFQR LVSKDSNRO KV HVMDLDK HNYYVEK UVE ZVNE YEVYVHFM VS KADH HDOR VU KAR FKMFSKDL, FSO D FP LVSUDORSK KAFK PZ VTS HPFMM LVSKEDINKDVS LFS YMFZ FS DPYVEKFSK YFEK DS DKH HNLLRHH. D KENHK KAFK ZVNE XEVNY ERPFDSH LVSUDORSK KAFK DK LFS ORMDQRE VS DKH YEVPDHR. TDKA KAR HNYYVEK VU KAR IEDKDHA FSO FPREDLFS XVQRESPRSKH D KADSJ TR LVNMO INDMO HVPRKADSX RSKDERMZ SRT FSO RWKERPRMZ YVTREUNM, AVTRQRE KAR KENR YVKRSKDFM LFS VSMZ IR PRK DU TR LFS RSHNER KVKFM HRLERLZ, FSO D TDMM AFQR KV ERMZ VS ZVN KV YREHNFOR LAFEMRH SVK KV HYRFJ VU VNE ORHDXSH TDKA FSZVSR VNKHDOR VU VNE LDELMR. UVE ADH VTS YFEK, LAFEMRH DH LADRUMZ DSKRERHKRO DS KAR HNLLRHH VU ADH KVNE, FSO TADMR AR TDMM YMFZ FS DPYVEKFSK EVMR DS YREHNFODSX DSQRHKVEH KV GVDS VNE HLARPR FSO YVMDKDLDFSH KV HNYYVEK DK, DK DH DPYVEKFSK KAFK AR DH FMHV FIMR KV RSGVZ KAR UENDKH VU ADH ERFODSX YREUVEPFSLRH. AR DSQRHKH PNLA VU ADPHRMU DS KAVHR ERFODSXH FSO DH DSLMDSRO KV VQREKDER ADPHRMU. D KENHK KAFK ZVN FSO ZVNE UEDRSOH TDMM VUURE ADP KAR HNYYVEK KAFK D TVNMO VUURE DU D LVNMO IR KARER TDKA ADP. TDKAVNK KAFK HNYYVEK D URFE KAFK AR TDMM AFQR SV RSREXZ MRUK KV YEVPVKR VNE YEVGRLK. ZVNE UEDRSO, LAFEMRH IFIIFXR
""".upper()

trigam_inator = trigram()

ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "RemoveSpaces": False, #sm more readable when u do
    "Ready" : True,
    "AutoSolve" : True,
    "superfun" : True
}
decryptionReady = True

result = ""
punctuation = [",","."]
if decipherData["RemoveSpaces"]: string=string.replace(" ","")
for char in string:
    if char.isalpha() or char == " " or char in punctuation:
        result+=char
string = result

if ReverseString:
    string = string[::-1]

print(f"{GREEN}String length: {len(string)}{RESET}")


if __name__ == "__main__":
    bestKeys = []
    for i in range(5):
        print(f"{BLUE}")
        initial_temp = 10
        max_iterations = 5000 #normally it solves it in under 5000 but better safe than sorry
        cooling_rate = 0.9996

        alphabet = list(st.ascii_uppercase) #generate random key
        current_key = ""
        for j in range(26):
            current_key+=str(random.choice(alphabet))
            alphabet.remove(current_key[-1])

        current_score = trigam_inator.score(decrypt(string, current_key))

        best_key = current_key
        best_score = current_score

        temperature = initial_temp

        accepted_moves = 0

        for iteration in range(max_iterations):
            new_key = shuffleKey(current_key)
            new_score = trigam_inator.score(decrypt(string, new_key))
            
            #calc score diff
            diff = new_score - current_score
            
            if diff > 0:
                current_key = new_key
                current_score = new_score
                accepted_moves += 1
                
                if current_score > best_score:
                    best_key = current_key
                    best_score = current_score
            else:
                #accept worse solutions with probability based on temperature
                if temperature == 0:
                    continue
                acceptance_probability = math.exp(diff / temperature) #chatgptd math icl
                if random.random() < acceptance_probability:
                    current_key = new_key
                    current_score = new_score
                    accepted_moves += 1
            
            temperature *= cooling_rate
            
            if (iteration + 1) % 1000 == 0: #blank screens do be scary
                acceptance_rate = (accepted_moves / 1000) * 100
                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Acceptance = {acceptance_rate:.1f}%, Key = {best_key}")
                decrypted_sample = decrypt(string, best_key)[:120]
                print(f"Current decryption: {decrypted_sample}...\n")
                accepted_moves = 0
            elif (iteration+1) % 250 == 0 and (iteration+1) // 250 <5:
                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Key = {best_key}")
                decrypted_sample = decrypt(string, best_key)[:120]
                print(f"Current decryption: {decrypted_sample}...\n")
        print(f"\033[1m{RED}LOOP {i+1} INFO: ")
        print(f"{MAGENTA}Recommended key: {best_key}")
        print(f"Score: {best_score} {RESET}\n")
        print(f"Decryption: \n{GREEN}{decrypt(string,best_key)}{RESET}")

        bestKeys.append(best_key)
    lowestChis = []
    for key in bestKeys:
        lowestChis.append([chiSquared(decrypt(string,key)),key])
    lowestChis = sorted(lowestChis, key=lambda data: data[0])

    print("\n"+"="*46+"\n")
    print(f"\033[1m{RED}MOST LIKELY KEY IS: {lowestChis[0][1]}")
    print(f"Most likely decryption is:\n {GREEN}{decrypt(string,lowestChis[0][1])}")
    print(f"\n\033[35mOther likely data: {lowestChis}{RESET}")
from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

from cipherTools import Affineshift,recommendedShiftChiSquared # type: ignore

#Editable toggles and shit
string = """
PZ ORFE XERSQDMMR, D PNHK FYVMVXDHR UVE LAFEMRH, AR DH F XVVO PFS, INK LFS IR DEFHLDIMR, FSO KEFQRM ERFMMZ OVRH SVK HNDK ADP. D ERFO ADH MRKKRE KV ZVN TDKA HVPR LVSLRES (KAFSJ ZVN UVE HRSODSX PR F LVYZ), HRRDSX KAFK DK ORPVSHKEFKRH F MVTSRHH DS ADH HYDEKH, INK D LFS FHHNER ZVN KAFK AR DSKRSOH VSMZ KAR IRHK UVE VNE RSORFQVNE. DK KVVJ KAR LVPIDSRO RUUVEKH VU PZHRMU FSO MVEO OREIZ KV LVSQDSLR ADP VU KAR EDXAKSRHH VU VNE YMFS, INK TADMR AR DH UNMMZ LVPPDKKRO KV VNE LFNHR, AR DH SVK RSKDERMZ FK RFHR TDKA VNE PRKAVOH. D AFQR LVSKDSNRO KV HVMDLDK HNYYVEK UVE ZVNE YEVYVHFM VS KADH HDOR VU KAR FKMFSKDL, FSO D FP LVSUDORSK KAFK PZ VTS HPFMM LVSKEDINKDVS LFS YMFZ FS DPYVEKFSK YFEK DS DKH HNLLRHH. D KENHK KAFK ZVNE XEVNY ERPFDSH LVSUDORSK KAFK DK LFS ORMDQRE VS DKH YEVPDHR. TDKA KAR HNYYVEK VU KAR IEDKDHA FSO FPREDLFS XVQRESPRSKH D KADSJ TR LVNMO INDMO HVPRKADSX RSKDERMZ SRT FSO RWKERPRMZ YVTREUNM, AVTRQRE KAR KENR YVKRSKDFM LFS VSMZ IR PRK DU TR LFS RSHNER KVKFM HRLERLZ, FSO D TDMM AFQR KV ERMZ VS ZVN KV YREHNFOR LAFEMRH SVK KV HYRFJ VU VNE ORHDXSH TDKA FSZVSR VNKHDOR VU VNE LDELMR. UVE ADH VTS YFEK, LAFEMRH DH LADRUMZ DSKRERHKRO DS KAR HNLLRHH VU ADH KVNE, FSO TADMR AR TDMM YMFZ FS DPYVEKFSK EVMR DS YREHNFODSX DSQRHKVEH KV GVDS VNE HLARPR FSO YVMDKDLDFSH KV HNYYVEK DK, DK DH DPYVEKFSK KAFK AR DH FMHV FIMR KV RSGVZ KAR UENDKH VU ADH ERFODSX YREUVEPFSLRH. AR DSQRHKH PNLA VU ADPHRMU DS KAVHR ERFODSXH FSO DH DSLMDSRO KV VQREKDER ADPHRMU. D KENHK KAFK ZVN FSO ZVNE UEDRSOH TDMM VUURE ADP KAR HNYYVEK KAFK D TVNMO VUURE DU D LVNMO IR KARER TDKA ADP. TDKAVNK KAFK HNYYVEK D URFE KAFK AR TDMM AFQR SV RSREXZ MRUK KV YEVPVKR VNE YEVGRLK. ZVNE UEDRSO, LAFEMRH IFIIFXR
"""

ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi"
}
decryptionReady = True

result = ""

for char in string:
    if char.isalpha() or char == " ":
        result+=char
string = result

if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"String length: {len(string)}")

def recommendedShift(args: dict, mode = "chi")-> list:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])
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

if decryptionReady:
    for i,block in enumerate([string]):
        args = {
            "string" : block,
            "info" : True
        }
        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            shiftNum = [int(i) for i in (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")).split(",")] or [1,0]
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        if shiftNum:
            string = Affineshift(block,shiftNum).lower()
    if string.islower():
        print(BLUE + string + RESET)
    else:
        print(RED + string + RESET)

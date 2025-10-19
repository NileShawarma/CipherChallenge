from collections import Counter
import numpy

def frequencyAnalysis(string: str) -> dict:
    freqs = Counter(string)
    print(sorted(freqs.items(), key=lambda thingy: thingy[0]))
def recommendedShiftFrequencyAnalysis(string: str, info = False) -> int:
    frequencies = frequencyAnalysis(string)

    distance = ord("E") - ord(frequencies[-1])
    if distance < 0: distance = 26+distance

    if info:
        print(frequencies[-1])
        print(frequencies[-2])
        print(frequencies[-3])
        print(frequencies[-4])

    return distance
def Affineshift(text: str,key: list) -> str:
    result = ""
    multi = key[0]
    shift = key[1]
    for i in range(len(text)):
        char = text[i]
        if not char.isalpha():
            result += char
            continue
        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((((ord(char)-65)*multi)+(shift))%26+65)
        # Encrypt lowercase characters
        else:
            result += chr( ( ( (ord(char)-97) *multi) +shift) % 26 + 97)

    return result
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
    freqs = Counter(text.replace(" ",""))
    length = len(text)

    total = 0
    for letter, freq in freqs.items():
        try:
            total +=((freq-(english_letter_frequencies[letter.upper()]*length))**2)/english_letter_frequencies[letter.upper()]
        except:
            pass
    return total
def recommendedShiftChiSquared(string: str, info = False) -> int:
    minChi = [10**10,0]
    allChis = []
    possibleMultis = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    for j in possibleMultis:
        for i in range(26):
            chi = chiSquared(Affineshift(string,[j,i]))

            if chi<minChi[0]:
                minChi = [chi,[j,i]]
            allChis.append([chi,[j,i]])
    
    if info:
        allChis=sorted(allChis, key=lambda thingy: thingy[0])
        print("Chi level, and likely keys:")
        print(allChis[0])
        print(allChis[1])
        print(allChis[2])

    return minChi[1]
def ic(self):
    freqs = Counter(self)
    length = len(self)

    ioc = sum([value*(value-1) for value in freqs.values()])/(length*(length-1))
    return ioc
def inverseText(string: str) -> str:
    result = ""
    for char in string:
        keyCode = 90-(ord(char)-65)
        result += chr(keyCode)
    return result
def matrixMultiplier(MatA : list, MatB : list) -> list:
    """Eg
    1 4 7     1
    2 5 8     2
    3 6 9     3

    = 1*1 + 4*2 + 7*3
      2*1 + 5*2 + 8*3
      3*1 + 6*2 + 9*3
    
    = 30
      36
      42
    """

    num_columns_mat_a = len(MatA[0])
    num_rows_mat_a = len(MatA)

    num_rows_mat_b = len(MatB)
    num_columns_mat_b = len(MatB[0])

    if num_rows_mat_b!=num_columns_mat_a:
        raise ValueError("Matrices are not compatible!")
    
    resultMat =[[0 for __ in range(num_columns_mat_b)] for _ in range(num_rows_mat_a)]

    #print(num_columns_mat_a)
    #print(num_rows_mat_a)
    ##print(num_columns_mat_b)
    #print(num_rows_mat_b)
    for ___ in range(num_columns_mat_a):
        for __ in range(num_rows_mat_a):
            for _ in range(num_columns_mat_b):
                #print(f"{_}")
                #print(f"ResultMat[{__},{_}] += {MatA[__][___]} (MatA[{__},{___}]) *{MatB[__][_]} (MatB[{__},{_}])")
                resultMat[__][_] += MatA[__][___]*MatB[___][_]
                #print(resultMat)
    return resultMat
def baseN_Inverse(num: int, base: int = 26)-> int:
    for i in range(1,base):
        if (num*i)%base == 1:
            return i
    return None
def inverseMatrixMod26(MatA: list):
    length = len(MatA)
    determinant = int(round(numpy.linalg(MatA)))
    return numpy.linalg.inv(numpy.array(MatA))
if __name__ == "__main__":
    MatA = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]

    MatB = [
        [1,2,2],
        [3,4,12],
        [5,6,30]
    ]
    resultMat = numpy.array(matrixMultiplier(MatA,MatB))
    print(resultMat)
    print(matrixMultiplier(MatA,MatB))

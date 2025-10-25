from collections import Counter
import string as st
import os 
import sys
import math
import random
from time import localtime, strftime

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)

from cipherTools import Affineshift,recommendedShiftChiSquared,ic,chiSquared,recommendedShiftFrequencyAnalysis # type: ignore
"""
Idea: a script that allows us to easily view data of a ciphertext,
      perform actions like shifts or transpositions
      rollbacks
      logging to memory files
"""
STORAGE_PATH = os.path.join(script_dir,"..","Test","Data","Manipulator","storage.txt")

class bigDaddyDecrypter():
    def __init__(self,cipherText: str,openWith = 0, args :dict = {}):
        global STORAGE_PATH
        self.text = cipherText
        self.actionsCompleted = 0
        self.allActions = [] 
        """
        Each element of self.allActions follows the structure: 
            {"newText" : ... ,"Type" : ... ,"Time" : ...} + extras depending on type
        Type: Caesar, is given "ShiftKey"
        Type: Affine, is given "AffineKey"
        Type: Substitution, is given "SubKey"
        Type: Vigenere, is given "VigKey" (optional), "keyLength", "ShiftList"
        """

        if openWith:
            STORAGE_PATH = os.path.join(os.path.dirname(STORAGE_PATH),openWith)

            with open(STORAGE_PATH,"r") as file:
                for line in file:
                    if line[0] == "|":  #We've found the start of an update
                        dataPacket = {}
                        components = line[1:-1].split("|")
                        components = [header.split(";") for header in components]

                        for part in components:
                            if len(part) == 2:
                                dataPacket[part[0].strip()] = part[1].strip()
                    
                    elif line[0] == "-": #We've found the end of an update
                        self.allActions.append(dataPacket)
                    else: #We need to add update details
                        components = line.split(";")
                        dataPacket[components[0].strip()] = components[1].strip()
            self.text = self.allActions[-1]["newText"]

            """
            Executing args
            """

            if "OVERRIDE" in args.keys():
                if args["OVERRIDE"]:
                    self.text = cipherText

            self.saveUpdate(
                {
                    "Type" : "__init__, Entered new storage log",
                    "newText" : self.text,
                    "Message" : f"Initialised decrypter, now utilising {openWith}"
                }
            )
        else:
            self.saveUpdate({
                "Type" : "__init__",
                "newText" : self.text,
                "Message": f"Initialised decrypter at default storage"
            })
    def saveUpdate(self,args:dict):
        with open(STORAGE_PATH,"+a") as file:
            currentTime = strftime("%H:%M",localtime())
            action = args["Type"]

            file.write(f"| Edit No.{self.actionsCompleted} | Time ; {currentTime} | Type ; {action} |\n")
            
            self.actionsCompleted += 1
            
            message = args["newText"].replace("\n","")
            file.write(f"newText ; {message}\n")

            basicTitles = ["Type","newText"]
            dataPackage = {"newText":message,"Type":action,"Time":currentTime}

            for key, data in args.items():
                if key in basicTitles:
                    continue

                file.write(f"{key} ; {data}\n")
                dataPackage[key] = data
            
            self.allActions.append(data)

            file.write("-"*66+"\n")
    def rollback(self,stages):
        self.text = self.allActions[-1-(stages)]["newText"]

        self.saveUpdate({
            "newText" : self.text,
            "Type" : "Rollback",
            "RollbackStages" : stages
        })
    def affine(self,shift:list):
        self.text = Affineshift(self.text,shift)
        self.saveUpdate(
            {
                "Type" : "Affine",
                "newText" : f"{self.text}",
                "AffineKey" : shift
            }
        )
    def caesar(self,shift:int):
        self.text = Affineshift(self.text,[1,shift])
        self.saveUpdate(
            {
                "Type" : "Caesar",
                "newText" : f"{self.text}",
                "ShiftKey" : shift
            }
        )
    def substitution(self,key:str):
        ALPHABET = st.ascii_lowercase

        if len(key) < 26: #Converts keyword into an actual key
            realKey = key
            tempAlpha = list(ALPHABET.upper())
            for char in key:
                if char==key[-1]:continue
                tempAlpha.remove(char)
            
            lastChar = key[-1]
            index = tempAlpha.index(lastChar)
            tempAlpha.remove(char)
            for _ in range(index,len(tempAlpha)):
                realKey+=tempAlpha[_]
            
            for _ in range(0,index-1):
                realKey+=tempAlpha[_]
            key=realKey
        
        plaintext = ""
        decryption_map = {c: p for p, c in zip(ALPHABET, key)} #assigns each enciphered letter its corresponding plaintext 
        for char in self.text:
            if char in decryption_map:
                plaintext+= decryption_map[char]
            else:
                plaintext += char
            
        self.text = plaintext

        self.saveUpdate(
            {
                "Type" : "Mono-Substitution",
                "newText" : f"{self.text}",
                "SubKey" : key.upper()
            }
        )
    def vigenere(self,key=""):
        """
        removes punctuation and spaces
        applies the key to the text, not decrypt with known key, to accomplish this you must inverse the key
        """
        string = self.text.replace(" ","").replace("\n","")
        res = ""
        for char in string:
            if char.isalpha():
                res+=char
        string = res



cipherText = """
GRV XKF TXXFQXLRQ RG JFQFVTO EREJF PV EREJF, AKLOF L ITQQRX IOTLP XR KTZF VFIRZFVFE GYOOC GVRP XKF VLJRYVW RG PC MRYVQFC, L KTZF QRA TEMYWXFE XR CRYV IOLPTXF TQE KTZF HFJYQ XR FWXTHOLWK PC VRYXLQF. L KRSF CRY ALOO QRX XTNF LX HTEOC XKTX L TP VFOYIXTQX XR TJVFF XR CRYV VFUYFWX XR FBSFELXF PC ZLWLX XR ATWKLQJXRQ, HYX L TP QR ORQJFV T CRYQJ PTQ, TQE PC SFVGRVPTQIFW VFUYLVF IRQWLEFVTHOF FQFVJC GVRP PF. TJF LW XKF XKLFG RG XLPF, TQE QRQF RG YW NQRA KRA UYLINOC LX LW WXROFQ GVRP YW. L PYWX ER AKTX L ITQ XR PTVXLTO XKTX PRWX SVFILRYW VFWRYVIF. RYV PYXYTO GVLFQE, PV HTHHTJF, KTW IRPPFQEFE CRY XR PF, TQE RYV RAQ SVLPF PLQLWXFV KTW XTNFQ STLQW XR FBSOTLQ XR PF XKF LPSRVXTQIF RG CRYV PLWWLRQ, KRAFZFV L GTLO XR WFF KRA VFTVVTQJLQJ PC WIKFEYOF ALOO ER TQCXKLQJ PYIK XR WSFFE XKF SVRJVFWW RG AKTX PYWX QFIFWWTVLOC HF T ORQJ-XFVP LQZFWXPFQX RG ITSLXTO TQE VFWRYVIFW. L KTZF SVRPLWFE XKTX L ALOO ER AKTX L ITQ XR TWWLWX CRY, HYX L PYWX IRQWLEFV PC RAQ KFTOXK TQE AFOGTVF LG L TP XR IRPSOFXF XKLW XRYV. PTC L TOWR VFPTVN XKTX LG XKF ARVN RQ AKLIK CRY TVF FPHTVNFE LW XVYOC TW WFIVFX TW CRY TQE HTHHTJF WFFP XR HFOLFZF, XKFQ XKF YWF RG TQILFQX ILSKFVW ERFW QRX PFFX XKTX QFFE. L KTZF XTNFQ XKF OLHFVXC RG YWLQJ WRPFXKLQJ T OLXXOF PRVF TSSVRSVLTXF LQ XKLW OFXXFV TQE ARYOE WYJJFWX XKTX SFVKTSW AF YWF XKLW PFXKRE GRV RYV GYXYVF IRPPYQLITXLRQW. CRYVW WLQIFVFOC, IKTVOFW ELINFQW
""".replace("\n","")
cipherText = bigDaddyDecrypter("","storage.txt")
print(cipherText.text)

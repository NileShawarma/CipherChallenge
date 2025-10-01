from itertools import permutations

string = "ANROH AESTM VEYES HAEKS TKCEH VRTEA EEHRK NLNND EBMSS OBOGN HAIOR GLASU SAFAU AIUAA ONAEG EEPTM DFLTE HESOE ARFME EOTAE LSAPA ATLIK ENHAI SETIZ AAEAH EOBOT TNTDR TLTFA SVNED SRNWT ASETO DLLNY DELOS ELLTP IKEHW LOOTC TTAEY ITSRR HANER MAIAS EDDAI ADEAI MBTLO RUAUA NUHNT MTTMO TGWUS LTSOF YASED UALSO ODESY SNUNA GDAPO DAEEI SLGEC KBUCR HUIEG OYIRI PEMNR DLTTN EPHEE FIASE MTAEO IILEE GATNR OEEIM YTCDN UETEH EROIE NNSIR YTTLE TUSTG GCMSU TCTAH EETIA IESDA HENSG VOERS NHSTI ORTDB HETSA EEBHE RTLEY NSGEE HEREH TOETH EDTTE EICEE STATT ELIFW OIEPB MEUEJ IDOHT TIAED VMHUS SDTSN OEIKA SCDTI LVCTC EASCV EDNNI EIOTU TLRTO SEDWA HOURE EITIA HEHAF CTBIT SYMNO TREOF DTELA ONUOA KMSCI DESHT STISE RSTSU BGELH XEIYH EUMIT NTHAL ACOYX ODIAT AEHLD AAMFL EOGSA NATRJ IAMVN IMGAT TRIAN ICNWH SBUIT YLCTE IEEDW BESOF HOESD AIOSC SFINO MUENT KETUF NOILF ASVNB ESSFT OSESV NAWOR IPOFH AEBHE TTLVD NOEBT BLUAK ECECF FADMS AONIE ACOER ODEHE EDNIH VHYNE PVAHO METTL AWICA ITWHE GEEHA OTATE EHLER EHILC HAGMR MVREE TIGYO ETFAR OEEIY OSIDT THADT OSOOU TIASI OHNUT SIRMA NRCRT RYRCI MIDDE EICUH CTDIW NDHNT LYAEB HUOPR WNOME EATTL EEAEK NNDOG USEAF IDETS ABAOK EANHH HVAND HSCGT HMTAD LTEIR OFAEE HHEFE MAOEA LLCOD AAEEH EIODT EMMAE MDPEH NSETW HAISN ILRIK BHAIF AOHOK NTSEI CNAAL POHHS NCREE EMTHD EYGTR FEIBO OHGSE COILT EHENT IKGGN SHTIS EITTR TIKAG CELNT RNREE AIRCO UNMSG EERHO VNRLN IKNNT SHNEM UIWSS WBOTI PIFEI TESEE OLETT THAAN CENOD IARLV ETNNR UTCOD TAAAS TBPEA ROTIA NAYAA MTEWN ITTHO PNLDR OTHEW OTNLJ ICOMN YMBIU YENIA WTHUN NREEO HLDFW GCTWE TATID OKOTT EEHUF IWFHR CSTEF TIISD AFIAR DAAEH AEEOO UDASU SNTSA RDHIY NMEOP RENRC EUCSF ONAHL BCTEE ECHEI ETTGE SHAEB HHOMT HETTC TTBMS HMRDA ALIDT MNIEO IAOST ELESH LBPNT OLNEM RIEBO TNIWO TRMHR PUUGW TCUTN ETTHG NIAVE HINII"



string = "".join(string.split(" "))[::1]

print(len(string))
input()

def chunkBreaker(string: list, length: int, readMode = "row") -> list:
    numChunks = len(string)//length
    match readMode:
        case "row":
            chunks=[]
            for index in range(0,len(string)-length+1,length):
                chunks.append([string[index:index+length]])
            return chunks
        case "column":
            chunks = [[""] for j in range(numChunks)]#None for i in range((length))] for j in range(numChunks)]

            for index in range(0,len(string)):
                listNumber = index%(numChunks) 
                chunks[listNumber][0] += string[index]            
            return chunks

def swapValues(array: list,key: list) -> list:
    newArray = [None for i in array[0]]

    for index,value in enumerate(key):
        newArray[index] = array[0][value]

    return newArray

def all_full_permutations(lst):#chatgpt'd code here ibr rest is clean
    return [list(p) for p in permutations(lst, len(lst))]

while True:
    testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
    chunkLength = 5
    cribs = ["dynamix","citadelle","pds", "syndicate","gravitational", "waves","jamelia","martin","seismological","phenomenon","neutron", "star"]

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

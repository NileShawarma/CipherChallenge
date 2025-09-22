import configparser
import pathlib

STORAGE_PATH = str(pathlib.Path(__file__).parent.parent / "Data/storage.ini") #"Test/Data/storage.ini"

def createStorage():
    config = configparser.ConfigParser()

    Categories = ["Substitution","Caesar","Affine","Transposition"]
    SubCategories = ["Key","CipherText"]

    config.read(STORAGE_PATH)

    if pathlib.Path(STORAGE_PATH).exists():
        config["Hello"] = {"Test":"test"}
    else:
        config.read(STORAGE_PATH)

        config["Header"] = {"Opened":True}
                
        for category in Categories:
            data = {}
            for subcategory in SubCategories:
                data[subcategory] = ""
            config[category] = data
        
        with open(STORAGE_PATH,"w") as file:
            config.write(file)

def writeToStorage(newValue:str = "test" , key: str = "Test" , title: str = "Hello"):
    config = configparser.ConfigParser()
    config.read(STORAGE_PATH)
    
    config[title][key] = newValue

    with open(STORAGE_PATH,"w") as file:
        config.write(file)

def readFromStorage(key: str = "Test", title: str = "Hello"):
    config = configparser.ConfigParser()
    config.read(STORAGE_PATH)

    return config[title][key]

if __name__ == "__main__":
    createStorage()

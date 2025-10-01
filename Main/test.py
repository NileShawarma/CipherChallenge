import tkinter as tk
import string
import Modules.Text as Text

alphabet = "abcdefghijklmonpqrstuvwxyz"

SubstitutionPageData = {"Table":0,"KeyData":0,"CipherText":0}

currentActiveCipher = None

def clear_frame():
    global currentActiveCipher
    global SubstitutionPageData
    match currentActiveCipher: #Saves data
        case "Substitution":
            DecryptionKey = ""
            for key in SubstitutionPageData["KeyData"][0]:
                if key.get() == "":
                    DecryptionKey+="-"
                else: DecryptionKey+=key.get()
            Text.writeToStorage(DecryptionKey,key="key",title="Substitution")
            Text.writeToStorage(SubstitutionPageData["CipherText"].get("1.0","end"),"ciphertext","Substitution")

    """Clear all widgets from the content frame."""
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_home():
    clear_frame()
    tk.Label(content_frame, text="🏠 Home Page", font=("Arial", 18)).pack(pady=10)

def move_to_next(event, row, col):
    global SubstitutionPageData
    """Move focus to the next entry cell in the row."""
    if event.keysym.upper() in alphabet.upper():  
        SubstitutionPageData["KeyData"][row][col].delete(0,tk.END)
        SubstitutionPageData["KeyData"][row][col].insert(0,event.keysym.upper()) #Changes the input to be a capital letter to conform to conventions

        try:
            if decryptionWindowOpen:
                decrypt("substitution", table_frame.nametowidget("cipherInput")) #Every time we update a letter to our key we decrypt again
        except: pass #if the window isnt even open we js pretend nothing ahppened
        next_col = col + 1
        if next_col < 26:  # stay within range 
            next_entry = SubstitutionPageData["KeyData"][row][next_col]
            next_entry.focus_set() #be super cool and change the focussed widget to the next one if we type a letter

def cipherTextUpdate(event): pass

def open_new_window(title = "New Window"):
    """Opens a new window showing some text."""
    new_win = tk.Toplevel(root)
    new_win.title(title)
    new_win.geometry("400x200")

    return new_win

def decrypt(cipherType,cipherInput):
    global decrypted_text_win 
    global decryptionWindowOpen
    global cipherText 
    cipherText = cipherInput.get("1.0","end")
    try:
        if not decryptionWindowOpen:
            decrypted_text_win = open_new_window(title=cipherType)
    except: 
        decrypted_text_win = open_new_window(title=cipherType)
        tk.Label(decrypted_text_win, text="Plaintext:", font=("Arial", 14), name="plainTextTitle").pack(pady=10)
        tk.Text(decrypted_text_win, font=("Arial", 12, "bold"), fg="blue", name="plainTextContent").pack(fill="both", expand=True,pady=20)
        
        scrollbar = tk.Scrollbar(decrypted_text_win, command=decrypted_text_win.nametowidget("plainTextContent").yview)
        scrollbar.pack(side="right", fill="y")

        decrypted_text_win.nametowidget("plainTextContent").config(yscrollcommand=scrollbar.set)
    decryptionWindowOpen = True

    decrypted_text_win.bind("WM_DELETE_WINDOW", lambda : globals().update({"decryptionWindowOpen",False}))

    match cipherType:
        case "substitution":
            subsitution_keys = {}

            for index, plainLetter in enumerate(string.ascii_lowercase): #Generate substitution key
                cipherLetter = SubstitutionPageData["KeyData"][0][index].get() 
                if cipherLetter.isalpha():
                    print(f"'{cipherLetter}' = {plainLetter}")
                    subsitution_keys[cipherLetter] = plainLetter
            
            unusedLetters = list(string.ascii_uppercase)
            for letter in subsitution_keys.keys():
                unusedLetters.remove(letter)
            unusedLetters = ", ".join(unusedLetters)

            table_frame.nametowidget("unusedLetters")["text"]="Unused letters: " + unusedLetters
            print(unusedLetters)
            cipherText = list(cipherText)
            print(cipherText)
            for index,letter in enumerate(cipherText): #Decrypt
                if letter in subsitution_keys.keys():
                    cipherText[index] = subsitution_keys[letter]
            cipherText = "".join(cipherText)

    decrypted_text_win.nametowidget("plainTextContent").delete("1.0","end")
    decrypted_text_win.nametowidget("plainTextContent").insert("1.0",cipherText)
def show_table():
    global SubstitutionPageData
    global currentActiveCipher
    clear_frame()

    SavedKey = Text.readFromStorage("key","Substitution")
    SavedCipherText = Text.readFromStorage("ciphertext","Substitution")
    
    currentActiveCipher = "Substitution"

    tk.Label(content_frame, text="Substitution Cipher", font=("Arial", 16, "bold")).pack(pady=10)
    global table_frame
    SubstitutionPageData["Table"] = table_frame = tk.Frame(content_frame, bg="#e0e0e0")  # light gray background
    table_frame.pack(expand=True, fill="both", padx=10, pady=0)

    header_font = ("Arial", 11, "bold")
    cell_font = ("Arial", 11)

    # Row 1: numbers 0–25 (header)
    for col in range(26):
        tk.Label(
            table_frame, text=str(col), font=header_font, width=5, height=2,
            relief="ridge", bg="#4a90e2", fg="white"
        ).grid(row=0, column=col, sticky="nsew")

    # Row 2: letters A–Z (header)
    for col, letter in enumerate(string.ascii_lowercase):
        tk.Label(
            table_frame, text=letter, font=header_font, width=5, height=2,
            relief="ridge", bg="#50c878", fg="white", 
        ).grid(row=1, column=col, sticky="nsew")

    # Row 3: user input cells
    SubstitutionPageData["KeyData"] = [[]]
    for col in range(26):
        bg_color = "#ffffff" if col % 2 == 0 else "#f9f9f9"  # alternating column colors
        entry = tk.Entry(
            table_frame, font=cell_font, width=6, justify="center",
            relief="ridge", bg=bg_color
        )
        entry.grid(row=2, column=col, padx=1, pady=1, sticky="nsew")
        entry.bind("<KeyRelease>", lambda e, r=0, c=col: move_to_next(e, r, c))
        entry.insert(0,SavedKey[col])
        SubstitutionPageData["KeyData"][0].append(entry)

    global substitutionCipherText

    substitutionCipherText = ""

    unusedLetters = tk.Label(table_frame, text="Unused letters: " +", ".join(list(alphabet.upper())), font=("Arial", 12, "bold"), name="unusedLetters")
    unusedLetters.grid(row=4, column=0, columnspan=24, rowspan=1, pady=10, padx=5, sticky="w")

    cipherInput = tk.Text(table_frame, font=("Arial", 10), width=135, name="cipherInput")
    cipherInput.insert("1.0",SavedCipherText)
    cipherInput.grid(row=5, column=0, columnspan=24, rowspan=5, pady=10, padx=5, sticky="w")
    cipherInput.bind("<KeyRelease>", lambda event: cipherTextUpdate(event))
    SubstitutionPageData["CipherText"] = cipherInput
    substitutionCipherText = cipherInput.get("1.0","end")
    
    decrypt_button = tk.Button(table_frame, text="Decrypt", command=lambda: decrypt("substitution",cipherInput))
    decrypt_button.grid(row=4, column=21, columnspan=5, pady=10, padx=5, sticky="e")
    # Make all columns expand equally
    for col in range(26):
        table_frame.grid_columnconfigure(col, weight=1)
def show_about():
    clear_frame()
    tk.Label(content_frame, text="ℹ️ About This App", font=("Arial", 18)).pack(pady=10)

Text.createStorage()
# Create main window
root = tk.Tk()
root.title("Dynamic Menu Example")
root.geometry("1000x600")  # Wide enough for 26 columns

# Create a menu bar
menubar = tk.Menu(root)

# Pages menu
pages_menu = tk.Menu(menubar, tearoff=0)
pages_menu.add_command(label="Home", command=show_home)
pages_menu.add_command(label="Table", command=show_table)
pages_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Pages", menu=pages_menu)

# Attach the menu bar
root.config(menu=menubar)

# Content frame (where page contents appear)
content_frame = tk.Frame(root)
content_frame.pack(expand=True, fill="both")

# Show default page
show_home()

# Run application
root.mainloop()

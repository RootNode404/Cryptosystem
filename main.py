from cryptography.fernet import Fernet
import os, time

# Supress warnings
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def encrypt():

    print(colors.OKBLUE +  "[!]" + colors.ENDC + "Entered Encryption Mode" + colors.OKBLUE +  "[!]" + colors.ENDC)

    # Find some files
    files = []

    # Ask the directory to scan
    directory_path = str(input("Path of Folder to Encrypt" + colors.OKBLUE + " ->  " + colors.ENDC))

    # Iterate through each item in the specified directory
    files_found = 0
    print("Scanning...")
    for root, _, file_names in os.walk(directory_path):
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            files.append(file_path)
            files_found += 1
            print(colors.OKBLUE + f"[{files_found}]" + colors.ENDC + f" {file_path}")

    print(f"Found " + colors.OKBLUE + str(files_found) + colors.ENDC + " file(s).")

    confirmiation = str(input("Do you want to continue? " + colors.OKBLUE + "All" + colors.ENDC + " the files in " + colors.OKBLUE + f"{directory_path}" + colors.ENDC + " will be encrypted. " + colors.OKBLUE + "[y/n] " + colors.ENDC))

    if confirmiation == "n":
        print(colors.FAIL + "Aborting..." + colors.ENDC)
        exit()
    elif confirmiation == "y":
        pass

    # Generate key
    key = Fernet.generate_key()
    # Write generated key to file
    with open("fernet_key.key", "wb") as thekey:
        thekey.write(key)

    print("Fernet Key file generated. Located at [" + colors.OKBLUE + "./fernet_key.key" + colors.ENDC + "]")

    time.sleep(1)
    print(colors.OKBLUE + "[!]" + colors.ENDC + " Starting Encryption " + colors.OKBLUE + "[!]" + colors.ENDC)
    time.sleep(1)

    # Iterate over each file and extract content for encryption
    file_count = 1
    for file in files:
        try:
            with open(file, "rb") as thefile:
                # Save the contents of the file
                print(
                    colors.OKBLUE + f"[{file_count}]" + colors.ENDC + f" Starting Encryption on " + colors.OKBLUE + f"[{file}]" + colors.ENDC + " ")
                contents = thefile.read()

            # Encrypt them
            contents_encrypted = Fernet(key).encrypt(contents)

            # Rewrite the encrypted content to the file
            with open(file, "wb") as thefile:
                thefile.write(contents_encrypted)
                print(colors.OKBLUE + f"[{file_count}]" + colors.ENDC + f" File " + colors.OKBLUE + f"[{file}]" + colors.ENDC + " Successfully Encrypted")
                file_count += 1

        except PermissionError as e:
            print(colors.FAIL + "[!]" + colors.ENDC + f" Failed to Encrypt " + colors.OKBLUE + f" [{file}]" + colors.ENDC + " -> Permission Error " + colors.FAIL + "[!]" + colors.ENDC)
    time.sleep(1)
    print(colors.OKBLUE + "[!]" + colors.ENDC + " Encryption Complete " + colors.OKBLUE + "[!]" + colors.ENDC)

def decrypt():

    print(colors.OKBLUE + "[!]" + colors.ENDC + "Entered Decryption Mode" + colors.OKBLUE + "[!]" + colors.ENDC)

    # Find some files
    files = []

    # Ask the directory to scan
    directory_path = str(input("Path of Folder to Decrypt" + colors.OKBLUE + " ->  " + colors.ENDC))

    # Iterate through each item in the specified directory
    files_found = 0
    print("Scanning...")
    for root, _, file_names in os.walk(directory_path):
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            files.append(file_path)
            files_found += 1
            print(colors.OKBLUE + f"[{files_found}]" + colors.ENDC + f" {file_path}")

    print(f"Found " + colors.OKBLUE + str(files_found) + colors.ENDC + " file(s).")

    # Confirmation dialog
    confirmiation = str(input("Do you want to continue? " + colors.OKBLUE + "All" + colors.ENDC + " the files and folders in " + colors.OKBLUE + f"{directory_path}" + colors.ENDC + " will be Decrypted. " + colors.OKBLUE + "[y/n] " + colors.ENDC))

    if confirmiation == "n":
        print(colors.FAIL + "Aborting..." + colors.ENDC)
        exit()
    elif confirmiation == "y":
        pass

    # Get the key from the file
    try:
        with open("fernet_key.key", "rb") as key:
            key = key.read()

    except FileNotFoundError:
        print(colors.FAIL + "[!]" + colors.ENDC + "Key File Not Found" + colors.FAIL + "[!]" + colors.ENDC)
        exit()
    print("Fernet Key file found. Located at [" + colors.OKBLUE + "./fernet_key.key" + colors.ENDC + "]")

    time.sleep(1)
    print(colors.OKBLUE + "[!]" + colors.ENDC + " Starting Decryption " + colors.OKBLUE + "[!]" + colors.ENDC)
    time.sleep(1)

    # Iterate over each file and extract content for decryption
    file_count = 1
    for file in files:
        try:
            with open(file, "rb") as thefile:
                # Save the contents of the file
                print(
                    colors.OKBLUE + f"[{file_count}]" + colors.ENDC + f" Starting Decryption on " + colors.OKBLUE + f"[{file}]" + colors.ENDC + " ")
                contents = thefile.read()

            # decrypt them
            contents_decrypted = Fernet(key).decrypt(contents)

            # Rewrite the encrypted content to the file
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
                print(colors.OKBLUE + f"[{file_count}]" + colors.ENDC + f" File " + colors.OKBLUE + f"[{file}]" + colors.ENDC + " Successfully Decrypted")
                file_count += 1

        except Exception as e:
            print(
                colors.FAIL + "[!]" + colors.ENDC + f"Failed to Decrypt [{file}]x`: {e}" + colors.FAIL + "[!]" + colors.ENDC)

    time.sleep(1)
    print(colors.OKBLUE + "[!]" + colors.ENDC + " Decryption Complete " + colors.OKBLUE + "[!]" + colors.ENDC)

def info():

    # General overview
    print("")
    print(colors.WARNING + "[!]" + colors.ENDC + "OVERVIEW" + colors.WARNING + "[!]" + colors.ENDC)
    print("""   A simple CLI application written in python that encrypts/decrypts data with a custom Fernet key. Obviously 
   """ + colors.WARNING +  "DO NOT" + colors.ENDC + """ use this app for real world security implementations. It is not 100% secure or reliable. Make sure that the data your
   encrypting is """ + colors.WARNING + "NOT IMPORTANT" + colors.ENDC +  """ as the the decryption process can be glitchy sometimes and result in data loss or corruption.""")
    print("Link to Github Repository -> " + colors.OKBLUE + "" + colors.ENDC)


    # Terms and conditions
    print("")
    print(colors.WARNING + "[!]" + colors.ENDC + "TERMS AND CONDITIONS" + colors.WARNING + "[!]" + colors.ENDC)
    print("  By using this application you accept to the following terms and conditions:")
    print(colors.OKBLUE + "    [1]" + colors.ENDC + " I am not responsible for any loss or corruption of data")
    print(colors.OKBLUE + "    [2]" + colors.ENDC + " Nor am I not responsible for any illegal use of this application")
    print(colors.OKBLUE + "    [3]" + colors.ENDC + " And you have to star my Github Repository for this project;)")

try:
    print(colors.OKBLUE + colors.BOLD + """
    ______                                         _                 
   |  ____|                                       | |                
   | |__     _ __     ___   _ __   _   _   _ __   | |_    ___   _ __ 
   |  __|   | '_ \   / __| | '__| | | | | | '_ \  | __|  / _ \ | '__|
   | |____  | | | | | (__  | |    | |_| | | |_) | | |_  |  __/ | |   
   |______| |_| |_|  \___| |_|     \__, | | .__/   \__|  \___| |_|   
                                    __/ | | |                        
                                   |___/  |_|                        
""" + colors.ENDC)

except SyntaxError as e:
    pass

print(colors.WARNING + "[!]" + colors.ENDC + " By using this Application you accept to the Terms and Conditions (See Info). " + colors.WARNING + "[!]" + colors.ENDC, end="\n\n")

# Initialize the main menu
main_menu = ("Encrypt", "Decrypt", "Info", "Exit")
count = 1

for item in main_menu:

    print(colors.OKBLUE + f"[{count}]" + colors.ENDC + f" {item}")
    count += 1
print("")
option_num = int(input("Choose an Option " + colors.OKBLUE + "-> " + colors.ENDC))

if option_num == 1:
    encrypt()
elif option_num == 2:
    decrypt()

elif option_num == 3:
    info()

elif option_num == 4:
    print(colors.FAIL + "Aborting...", end="")
    exit()


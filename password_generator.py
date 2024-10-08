from random import randint
import json
import os
import base64

def passwordGenerator(length, wantChar):
    password = ""


    for i in range(length):
        currentChar = (chr(randint(33, 127)))

        if (wantChar == False):
            while not (currentChar.isalpha()) and not (currentChar.isnumeric()):
                currentChar = (chr(randint(33, 127)))
                if (currentChar.isalpha()) or (currentChar.isnumeric()):
                    break

        password += currentChar
        
    return password


def main():

    userOption = input("Do you want to generate a password or view saved passwords? G for Generate. V for View: ")
    while (userOption.lower() != 'g') and (userOption.lower() != "generate") and (userOption.lower() != 'v') and (userOption.lower() != "view"):
        userOption = input("Invalid input. Please enter G for Generate or V for View: ")
    if (userOption.lower() == 'v') or (userOption.lower() == "view"):
        if not os.path.exists("passwords.json"):
            print("No passwords saved.")
            return
        else:
            with open("passwords.json", 'r') as file:
                passData = json.load(file)
                for key in passData:
                    print(key)
                file.close()
            passLabel = input("Which password would you like to view? ")
            with open("passwords.json", 'r') as file:
                passData = json.load(file)
                if passLabel in passData:
                    print("Password for " + passLabel + ": " + passData[passLabel]["Password"])
                    if passData[passLabel]["isEncrypted"]:
                        decrypt = input("Would you like to decrypt this password? Y for Yes. N for No: ").lower()
                        if decrypt == 'y' or decrypt == 'yes':
                            password = base64.b64decode(passData[passLabel]["Password"]).decode('utf-8')
                            passData[passLabel]["Password"] = password
                            passData[passLabel]["isEncrypted"] = False
                            print("Decrypted password: " + password)
                            with open("passwords.json", 'w') as file:
                                json.dump(passData, file)
                                file.close()
                    else:
                        print("Password is not encrypted. Would you like to encrypt it? Y for Yes. N for No: ")
                        encrypt = input().lower()
                        if encrypt == 'y' or encrypt == 'yes':
                            password = base64.b64encode(passData[passLabel]["Password"].encode('utf-8')).decode('utf-8')
                            passData[passLabel]["Password"] = password
                            passData[passLabel]["isEncrypted"] = True
                            print("Password has been encrypted. \nEncrypted password: " + password)
                            with open("passwords.json", 'w') as file:
                                json.dump(passData, file)
                                file.close()
                else:
                    print("No password for " + passLabel + " found.")
                file.close()
            return


    wantChar = False

    lengthInput = int(input("Enter the length of your password: "))

    wantSpecChar = input("""Do you want special characters?
Y for Yes. N for No: """)
    
    if (wantSpecChar.lower() == 'y') or (wantSpecChar.lower() == "yes"):
        wantChar = True

    password = passwordGenerator(lengthInput, wantChar)
    
    print("Your password is: " + password)

    passSave = input("""Do you want to save your password?
Y for Yes. N for No: """)
    if (passSave.lower() == 'y') or (passSave.lower() == "yes"):
        passLabel = input("What are you saving this password for? ")

        passEncrypted = input("Would you like to encrypt your password? Y for Yes. N for No: ").lower()
        if passEncrypted == 'y' or passEncrypted == 'yes':
            password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
            print("Password encrypted.")
            passEncrypted = True


        passDataCurrent = {
            passLabel : {"Password" : password, "isEncrypted": passEncrypted}
        }
        

        if not os.path.exists("passwords.json"):
            with open("passwords.json", 'w') as file:
                json.dump(passDataCurrent, file)
                file.close()

        else:
            with open("passwords.json", 'r+') as file:
                content = file.read()
                if not content:
                    file.seek(0)
                    json.dump(passDataCurrent, file)
                else:
                    passData = json.loads(content) if content else {}
                    if passLabel in passData:
                        updateConfirm = input("A password for " + passLabel + " has already been made. \nDo you want to overwrite it? ")
                        if (updateConfirm.lower() == 'y') or (updateConfirm.lower() == "yes"):
                            passData.update(passDataCurrent)
                            file.seek(0)
                            file.truncate()
                            json.dump(passData, file)
                    else:
                        passData[passLabel] = {"Password" : password, "isEncrypted": passEncrypted}
                        file.seek(0)
                        file.truncate()
                        json.dump(passData, file)
                file.close()
        
    
main()
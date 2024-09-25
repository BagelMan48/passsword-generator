from random import randint
import json
import os

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

        passDataCurrent = {
            passLabel : password
        }
        

        if not os.path.exists("password.json"):
            with open("password.json", 'w') as file:
                json.dump(passDataCurrent, file)
                file.close()

        else:
            with open("password.json", 'r+') as file:
                content = file.read()
                if not content:
                    file.seek(0)
                    json.dump(passDataCurrent, file)
                else:
                    passData = json.loads(content)
                    if passLabel in passData:
                        updateConfirm = input("A password for " + passLabel + " has already been made. \nDo you want to overwrite it? ")
                        if (updateConfirm.lower() == 'y') or (updateConfirm.lower() == "yes"):
                            passData.update(passDataCurrent)
                            file.seek(0)
                            file.truncate()
                            json.dump(passData, file)
                    else:
                        passData[passLabel] = password
                        file.seek(0)
                        file.truncate()
                        json.dump(passData, file)
                file.close()
        
    
main()
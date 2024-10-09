import sqlite3
from sqlite3 import Error
from random import randint
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

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def main():
    connection = create_connection("password.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS passwords (title TEXT, password TEXT, encrypted BOOLEAN)")

    userOption = input("Do you want to generate a password or view saved passwords? G for Generate. V for View: ")
    while (userOption.lower() != 'g') and (userOption.lower() != "generate") and (userOption.lower() != 'v') and (userOption.lower() != "view"):
        userOption = input("Invalid input. Please enter G for Generate or V for View: ")
    if (userOption.lower() == 'v') or (userOption.lower() == "view"):
        cursor.execute("SELECT title, password, encrypted FROM passwords")
        for row in cursor.execute("SELECT title, password FROM passwords"):
            print(row)
            
        passLabel = input("\nWhich password would you like to view? ")
        showPass = cursor.execute("SELECT password, encrypted FROM passwords WHERE title = ?", (passLabel,))
        result = showPass.fetchone()
        if not result:
            print("Password not found.")
            return
        print(result)
        if result[1]:
            decrypt = input("Would you like to decrypt this password? Y for Yes. N for No: ").lower()
            if decrypt == 'y' or decrypt == 'yes':
                password = base64.b64decode(result[0]).decode('utf-8')
                print("Decrypted password: " + password)
                cursor.execute("UPDATE passwords SET password = ?, encrypted = ? WHERE title = ?", (password, False, passLabel))
                connection.commit()
        else:
            encrypt = input("Would you like to encrypt this password? Y for Yes. N for No: ").lower()
            if encrypt == 'y' or encrypt == 'yes':
                password = base64.b64encode(result[0].encode('utf-8')).decode('utf-8')
                print("Encrypted password: " + password)
                cursor.execute("UPDATE passwords SET password = ?, encrypted = ? WHERE title = ?", (password, True, passLabel))
                connection.commit()

    else:
        wantChar = False

        lengthInput = int(input("Enter the length of your password: "))

        wantSpecChar = input("""\nDo you want special characters?
Y for Yes. N for No: """)
        
        if (wantSpecChar.lower() == 'y') or (wantSpecChar.lower() == "yes"):
            wantChar = True

        password = passwordGenerator(lengthInput, wantChar)
        
        print("Your password is: " + password)

        passSave = input("""\nDo you want to save your password?
Y for Yes. N for No: """)
        if (passSave.lower() == 'y') or (passSave.lower() == "yes"):
            passLabel = input("\nWhat are you saving this password for? ")

            passEncrypted = input("\nWould you like to encrypt your password? ").lower()
            if passEncrypted == 'y' or passEncrypted == 'yes':
                password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
                print("Password encrypted.")
                passEncrypted = True

            cursor.execute("SELECT 1 FROM passwords WHERE title = ?", (passLabel,))
            if cursor.fetchone():
                print(f"A password with {passLabel} already exists.")
                
                replaceConfirm = input("Would you like to replace it? ").lower()
                if replaceConfirm == 'y' or replaceConfirm == 'yes':
                    cursor.execute("UPDATE passwords SET password = ?, encrypted = ? WHERE title = ?", (password, passEncrypted, passLabel))
                    connection.commit()
                    print("Password updated.")
                    return
                
                else:
                    print("Password not saved.")
                    return
            
            cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (passLabel, password, passEncrypted))
            connection.commit()
            print("Password saved.")
        
    
main()
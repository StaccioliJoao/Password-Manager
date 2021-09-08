import mysql.connector as mysql
import random
import string
import requests
import hashlib
import pyperclip

database = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="password_manager",
    autocommit=True
)
cursor = database.cursor()

cursor.execute("CREATE DATABASE Password_Manager")
cursor.execute("CREATE TABLE logins (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, website VARCHAR(255),url VARCHAR(255),username VARCHAR(255), email VARCHAR(255), passcode varchar(255), masterpass VARCHAR(255))")
cursor.execute("CREATE TABLE masterpasswords (idMaster INT AUTO_INCREMENT PRIMARY KEY,masterpass VARCHAR(255))")


def create(masterhash):
    website = input('Type the name of the website to be registered:')
    simplepass = input('Type a password that will be used to generate a safe one:')
    password = createpassword(simplepass)
    pyperclip.copy(password)
    print('-' * 30)
    print('\nYour generated password has been created and copied to your clipboard\n')
    print('-' * 30)
    email = input('Type the email that this password will be linked to:')
    username = input('Type the username that will be used in the website:')
    url = input('Type the url to the website you are creating the password for:')
    insertquery = "INSERT INTO logins (website, url, username, email, passcode, masterpass) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (website, url, username, email, password, masterhash)
    cursor.execute(insertquery, values)


def find_accounts(masterhash):
    search_email = input('Please provide the email that you want to search accounts for:')
    search_query = "SELECT * FROM logins WHERE email = %s AND masterpass = %s"
    values = (search_email, masterhash)
    cursor.execute(search_query, values)
    result = cursor.fetchall()
    print('-' * 116)
    print('RESULTS')
    print('')
    for x in result:
        print('Website/App name:', x[1], " |", 'URL:', x[2], " |", 'Email:', x[4], " |", 'Username:', x[3], " |", 'Password:', x[5], '\n')
    print('-' * 116)


def find_website(masterhash):
    search_website = input('Please provide the Website/App name that you want to find the password for:')
    search_query = "SELECT * FROM logins WHERE website = %s AND masterpass = %s"
    values = (search_website, masterhash)
    cursor.execute(search_query, values)
    result = cursor.fetchall()
    print('-' * 116)
    print('RESULTS')
    print('')
    for x in result:
        print('Website/App name:', x[1], " |", 'URL:', x[2], " |", 'Email:', x[4], " |", 'Username:', x[3], " |", 'Password:', x[5], '\n')
    print('-' * 116)


def lookup(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)

    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return count


def createpassword(password):
    lower_case = string.ascii_letters
    upper_case = lower_case.upper()
    numbers = string.digits
    symbols = '~!@#$%^&*()-=_+[]{}|\\;\',./<>?'
    password_length = 16
    password_amount = 5
    passwordhash = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    random.seed(passwordhash)
    choice = lower_case + upper_case + numbers + symbols

    genned_passwords = []
    for x in range(password_amount):
        password = "".join(random.sample(choice, password_length))
        genned_passwords.append(password)

    for i in genned_passwords:
        count = lookup(i)
        if count:
            genned_passwords.remove(i)
        else:
            finalpassword = random.choice(genned_passwords)
            break

    return finalpassword


def printmenu():
    print('')
    print('1 -- Create new password')
    print('2 -- Find all websites/apps connected to an email')
    print('3 -- Find a password for a website/app')
    print('4 -- Exit')
    return input(':')


def getmaster():
    print("__________________________")
    master = input("\nType your master password:")
    print("\n__________________________")
    print('')
    masterhash = hashlib.sha512(str(master).encode("utf-8")).hexdigest()
    sql = "SELECT masterpass FROM masterpasswords WHERE masterpass = '%s'" % masterhash
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        if result[0] == masterhash:
            choice = printmenu()
            while choice != '4':
                if choice == '1':
                    create(masterhash)
                elif choice == '2':
                    find_accounts(masterhash)
                elif choice == '3':
                    find_website(masterhash)
                else:
                    print('Invalid Choice')

                print('')
                choice = printmenu()
    else:
        insertquery = "INSERT INTO masterpasswords (masterpass) VALUES (%s)"
        valores = (masterhash,)
        cursor.execute(insertquery, valores)
        print("New master password created")
        choice = printmenu()
        while choice != '4':
            if choice == '1':
                create(masterhash)
            elif choice == '2':
                find_accounts(masterhash)
            elif choice == '3':
                find_website(masterhash)
            else:
                print('Invalid choice')

            print('')
            choice = printmenu()


getmaster()

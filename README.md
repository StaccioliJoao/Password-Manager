# Python Password Manager
>A simples password manager, this was created as a project and is not intended to be used to store sensitive data!

## Demonstration
[![Watch the demo](https://img.youtube.com/vi/L9gWyBN1uh4/2.jpg)](https://youtu.be/L9gWyBN1uh4)

## Requirements:
* MySql Server
* Python Modules:
  * mysql-connector-python:
    ```
    pip install mysql-connector-python
    ```
  * Requests:
    ```
    pip install types-requests
    ```
  * pyperclip:
    ```
    pip install pyperclip
    ```
    
## How it Works:
The aplication works by first you put in a master password that you will remember and that password gets converted to a sha-256 hash and is checked if it's already in the database, if it's not in the database the password hash will be registered and you will get to the main program. Then if you decide to create a new password it will prompt you the website name, url, username used and a password that will be used to seed the random function and generate a unique password each time, all passwords that are generated are ran through the PWNED API to check if they have been leaked and if they havent been leaked the password is stored in the database and copied to the user clipboard.

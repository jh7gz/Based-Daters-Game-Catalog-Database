import mysql.connector
from enum import Enum

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "gameCatalogs"
)

mycursor = db.cursor()

authorization_list = ('Player', 'User', 'Creator')

class Authorization(Enum):
    PLAYER = "Player",
    USER = "User",
    CREATOR = "Creator"


def login():
    found = 0
    while found == 0:
        id = input("Please enter your Profile Name (enter 0 to quit or 1 to create a new account): ")
        if id == '0':
            quit()

        while id == '1':
            id = input("Please enter your new Profile Name : ")
            mycursor.execute("SELECT * FROM User WHERE Profile_Name = (%s)", (id,))
            for x in mycursor:
                found += 1
            if found == 0:
                psswrd = input("That Profile Name is available. Please enter a password.")
                first = input("Please enter your first name")
                last = input("Please enter your last name")
                middle = input("Please enter your middle initial")
                mycursor.execute("INSERT INTO User(Profile_Name,Password,F_name,M_Init,L_Name) VALUES (%s,%s,%s,%s,%s)", (id,psswrd,first,middle,last))
                db.commit()
                print("New account created, proceeding to login")
            if found != 0:
                print("That Profile Name is in use, please try again")
                id = '1'


        mycursor.execute("SELECT * FROM User WHERE Profile_Name = (%s)", (id,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That Profile Name does not exist. Please enter a valid profile name.")
    
    correct = 0
    while correct == 0:
        pswd = input("Please enter your password (enter 0 to quit): ")
        if pswd == '0':
            quit()
        mycursor.execute("SELECT * FROM Employee WHERE Profile_Name = (%s) AND Password = (%s)", (id, pswd))
        for x in mycursor:
            correct += 1
        if correct == 0:
            print("That password is not correct. Please enter the correct password.")



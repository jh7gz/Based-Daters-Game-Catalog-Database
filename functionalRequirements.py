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
        id = input("Please enter your Profile Name (enter 0 to quit): ")
        if id == '0':
            quit()
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

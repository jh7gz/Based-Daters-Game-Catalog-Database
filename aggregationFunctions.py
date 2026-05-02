import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = db.cursor()

def finishSetup():
    mycursor.execute("USE gameCatalogs")

def getNumInventories(playerID):

    mycursor.execute("SELECT COUNT(playerID) as quantity FROM USER_EDIT_INVENTORY")

    return mycursor.quantity
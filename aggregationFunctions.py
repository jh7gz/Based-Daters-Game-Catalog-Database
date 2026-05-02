import mysql.connector

db = None
mycursor = None

def connectDB():
    global db, mycursor

    db = mysql.connector.connect(
        host="localhost",
        user="SA",
        password="Database2026",
        database="gameCatalogs"
    )

    mycursor = db.cursor()

def getNumInventories(playerID):

    mycursor.execute("SELECT COUNT(playerID) as quantity FROM USER_EDIT_INVENTORY")

    return mycursor.quantity
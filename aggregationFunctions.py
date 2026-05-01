import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Database2026",
    database = "gameCatalogs"
)

mycursor = db.cursor()

def getNumInventories(playerID):

    mycursor.execute("SELECT COUNT(playerID) as quantity FROM USER_EDIT_INVENTORY")

    return mycursor.quantity
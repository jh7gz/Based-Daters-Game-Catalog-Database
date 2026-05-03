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

def checkQuantity(id: int):
    total = mycursor.execute("SELECT Overall_Quan FROM ITEM WHERE Item_ID = (%s)", (id,)) - mycursor.execute("SELECT SUM (Quantity) FROM CONTAINS_ITEM WHERE Item_ID = (%s)",(id,)) 
    return total

def printItemInfo(id: int):
    mycursor.execute("SELECT * FROM ITEM WHERE Item_ID = (%s)", (itemID,))
    itemInfo = mycursor.fetchall()
    itemID,itemCatID,itemWeight,itemNum,itemDesc,itemCat,itemRare,itemName,itemConsumable,itemResource,itemWA,itemUpgrade = itemInfo
    print(f"ID: {itemID}, Catalog ID: {itemCatID}, Name: {itemName},Weight: {itemWeight}, Quantity: {itemNum}, Category: {itemCat}")
    print(f"Rarity: {itemRare}, Is Consumable: {itemConsumable}, Is Resource: {itemResource}, Is Weapon or Armor: {itemWA}, Is Upgradable: {itemUpgrade}")
    print(f"Description: {itemDesc}")
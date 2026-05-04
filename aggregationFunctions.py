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
    mycursor.execute("SELECT Overall_Quan FROM ITEM WHERE Item_ID = (%s)", (id,)) 
    overall = mycursor.fetchone()[0]
    mycursor.execute("SELECT SUM(Quantity) FROM CONTAINS_ITEM WHERE Item_ID = (%s)",(id,)) 
    current = mycursor.fetchone()[0]
    if current is None:
        current = 0
    return overall - current

def printItemInfo(id: int):
    mycursor.execute("SELECT * FROM ITEM WHERE Item_ID = (%s)", (id,))
    itemInfo = mycursor.fetchall()
    itemID,itemCatID,itemWeight,itemNum,itemDesc,itemCat,itemRare,itemName,itemConsumable,itemResource,itemWA,itemUpgrade = itemInfo
    print(f"ID: {itemID}, Catalog ID: {itemCatID}, Name: {itemName},Weight: {itemWeight}, Quantity: {itemNum}, Category: {itemCat}")
    print(f"Rarity: {itemRare}, Is Consumable: {itemConsumable}, Is Resource: {itemResource}, Is Weapon or Armor: {itemWA}, Is Upgradable: {itemUpgrade}")
    if itemWA == 1:
        watype = mycursor.execute("SELECT WAType FROM ITEM_WEAPON_ARMOR_TYPE WHERE Item_ID = (%s)",(id,))
        print(f"Weapon/Armor Type: {watype}")
        warange = mycursor.execute("SELECT WARange FROM ITEM_WEAPON_ARMOR_RANGE WHERE Item_ID = (%s)",(id,))
        print(f"Weapon/Armor Range: {warange}")
        wadamage = mycursor.execute("SELECT Damage FROM ITEM_WEAPON_ARMOR_RANGE WHERE Item_ID = (%s)",(id,))
        print(f"Weapon/Armor Damage: {wadamage}")
    if itemConsumable == 1 or itemWA == 1:
        itemEff = mycursor.execute("SELECT Effect FROM ITEM_EFFECT WHERE Item_ID = (%s)",(id,))
        print(f"Item Effect: {itemEff}")
        constInc = mycursor.execute("SELECT Constant_Inc FROM ITEM_EFFECT WHERE Item_ID = (%s)",(id,))
        print(f"Inceased By: {constInc}")
        percInc = mycursor.execute("SELECT Percent_Inc FROM ITEM_EFFECT WHERE Item_ID = (%s)",(id,))
        print(f"Percent Increase: {percInc}")
        effectDur = mycursor.execute("SELECT Duration FROM ITEM_EFFECT WHERE Item_ID = (%s)",(id,))
        print(f"Effect Duration: {effectDur}")
    print(f"Description: {itemDesc}")


def findSumWeight():
    found = 0
    invenID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM INVENTORY")
        for x in mycursor:
            for y in x:
                print(y)
        inven = input("Which inventory would you like to know the amount of items.")
        if inven == '0':
            break
        
        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        
        for x in mycursor:
            found += 1
            invenID = x[0]

        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
    mycursor.execute("SELECT SUM(Weight) FROM CONTAINS_ITEM JOIN ITEM ON CONTAINS_ITEM.Item_ID = ITEM.Item_ID WHERE Inventory_ID = (%s)", (invenID,))
    total[0] = mycursor.fetchone()
    if total is None:
        total = 0
    return total

def findMaxWeight():
    found = 0
    invenID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM INVENTORY")
        for x in mycursor:
            for y in x:
                print(y)
        inven = input("Which inventory would you like to know the amount of items.")
        if inven == '0':
            break
        
        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        
        for x in mycursor:
            found += 1
            invenID = x[0]

        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
    mycursor.execute("SELECT MAX(Weight) FROM CONTAINS_ITEM  JOIN ITEM ON CONTAINS_ITEM.Item_ID = ITEM.Item_ID WHERE Inventory_ID = (%s)", (invenID,))
    max[0] = mycursor.fetchone()
    if max is None:
        max = 0
    return max

def findMinWeight():
    found = 0
    invenID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM INVENTORY")
        for x in mycursor:
            for y in x:
                print(y)
        inven = input("Which inventory would you like to know the amount of items.")
        if inven == '0':
            break
        
        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        
        for x in mycursor:
            found += 1
            invenID = x[0]

        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
    mycursor.execute("SELECT MIN(Weight) FROM CONTAINS_ITEM  JOIN ITEM ON CONTAINS_ITEM.Item_ID = ITEM.Item_ID WHERE Inventory_ID = (%s)", (invenID,))
    min[0] = mycursor.fetchone()
    if min is None:
        min = 0
    return min

def findCountItemsInventory():
    found = 0
    invenID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM INVENTORY")
        for x in mycursor:
            for y in x:
                print(y)
        inven = input("Which inventory would you like to know the amount of items.")
        if inven == '0':
            break
        
        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        
        for x in mycursor:
            found += 1
            invenID = x[0]

        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
    mycursor.execute("SELECT SUM(Quantity) FROM CONTAINS_ITEM WHERE Inventory_ID = (%s)", (invenID,))
    count = 0
    for x in mycursor:
        count+=1
    return count

def findCountItemsCatalog():
    found = 0
    catalogID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM ITEM_CATALOG")
        for x in mycursor:
            for y in x:
                print(y)
        catalog = input("Which item catalog would you like to know the amount of items.")
        if catalog == '0':
            return
                        
        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
                        
        for x in mycursor:
            found += 1
            catalogID = x[0]

        if found == 0:
            print("That item catalog does not exist. Please enter a valid catalog.")
    count = 0
    mycursor.execute("SELECT * FROM ITEM WHERE Catalog_ID = (%s)",(catalogID,))
    for x in mycursor:
        count+=1
    return count

def findCountInventories(id: int):
    count = 0
    mycursor.execute("SELECT * FROM USER_EDIT_INVENTORY WHERE User_ID = (%s)",(id,))
    for x in mycursor:
        count+=1
    return count

def findCountCatalogs(id: int):
    count = 0
    mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE Creator_ID = (%s)",(id,))
    for x in mycursor:
        count+=1
    return count

def findCountCreatorsEditCatalog():
    found = 0
    catalogID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM ITEM_CATALOG")
        for x in mycursor:
            for y in x:
                print(y)
        catalog = input("Which item catalog would you like to know the amount of editors.")
        if catalog == '0':
            return
                        
        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
                        
        for x in mycursor:
            found += 1
            catalogID = x[0]

        if found == 0:
            print("That item catalog does not exist. Please enter a valid catalog.")
        
    count = 0
    mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE Catalog_ID = (%s)",(catalogID,))
    for x in mycursor:
        count+=1
    return count


def findCountUsersEditInventory():
    found = 0
    invenID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM INVENTORY")
        for x in mycursor:
            for y in x:
                print(y)
        inven = input("Which inventory would you like to know the amount of editors.")
        if inven == '0':
            break
        
        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        
        for x in mycursor:
            found += 1
            invenID = x[0]

        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
    mycursor.execute("SELECT * FROM USER_EDIT_INVENTORY WHERE Inventory_ID = (%s)", (invenID,))
    count = 0
    for x in mycursor:
        count+=1
    return count

def getMaxWeightCatalog():
    found = 0
    catID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM ITEM_CATALOG")
        for x in mycursor:
            for y in x:
                print(y)
        catalog = input("Which catalog would you like to know the max weight of.")
        if catalog == '0':
            break
        
        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        
        for x in mycursor:
            found += 1
            catID = x[0]

        if found == 0:
            print("That catalog does not exist. Please enter a valid catalog.")
    mycursor.execute("SELECT MAX(Weight) FROM ITEM_CATALOG JOIN ITEM ON ITEM_CATALOG.Catalog_ID = ITEM.Catalog_ID WHERE ITEM.Catalog_ID = (%s)", (catID,))
    max[0] = mycursor.fetchone()
    if max is None:
        max = 0
    return max

def getMinWeightInventory():
    found = 0
    catID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM ITEM_CATALOG")
        for x in mycursor:
            for y in x:
                print(y)
        catalog = input("Which catalog would you like to know the max weight of.")
        if catalog == '0':
            break
        
        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        
        for x in mycursor:
            found += 1
            catID = x[0]

        if found == 0:
            print("That catalog does not exist. Please enter a valid catalog.")
    mycursor.execute("SELECT MIN(Weight) FROM ITEM_CATALOG JOIN ITEM ON ITEM_CATALOG.Catalog_ID = ITEM.Catalog_ID WHERE ITEM.Catalog_ID = (%s)", (catID,))
    min[0] = mycursor.fetchone()
    if min is None:
        min = 0
    return min
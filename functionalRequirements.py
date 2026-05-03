import mysql.connector
import aggregationFunctions as af
from enum import Enum

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = db.cursor()

def finishSetup():
    mycursor.execute("USE gameCatalogs")

def login():
    userid = 0
    found = 0

    while found == 0:

        id = input("Please enter your Profile Name (enter 0 to quit or 1 to create a new account): ")

        #quit on 0
        if id == '0':
            quit()

        # create new username
        while id == '1':

            id = input("Please enter your new Profile Name or type 0 to go back: ")

            if id == "0":
                found = 0
                break

            userid = mycursor.execute("SELECT User_ID FROM USERS WHERE Profile_Name = (%s)", (id,))

            for x in mycursor:
                found += 1

            if found == 0:
                psswrd = input("That Profile Name is available. Please enter a password: ")
                first = input("Please enter your first name: ")
                last = input("Please enter your last name: ")
                middle = input("Please enter your middle initial: ")
                
                while len(middle) > 1:

                    middle = input("Please input only middle initial: ")


                try:
                    mycursor.execute("INSERT INTO USERS(Profile_Name,Password,F_name,M_Init,L_Name) VALUES (%s,%s,%s,%s,%s)", (id,psswrd,first,middle,last))
                    #db.commit()
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
                print("New account created, proceeding to login")

            if found != 0:
                print("That Profile Name is in use, please try again")
                id = '1'


        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s)", (id,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That Profile Name does not exist. Please enter a valid profile name.")
    

    correct = 0
    while correct == 0:
        pswd = input("Please enter your password (enter 0 to quit): ")
        if pswd == '0':
            quit()
        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s) AND Password = (%s)", (id, pswd))
        for x in mycursor:
            correct += 1
        if correct == 0:
            print("That password is not correct. Please enter the correct password.")

    return userid


    

def createCatalog(id: int):
    name = ""
    while name == "":
        name = input("What would you like the name of the Item Catalog to be?")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (name,))
        for x in mycursor:
            name = ""
            break
        if name == "":
            print("That item catlog already exists. Please enter a valid new catalog name.")
       
    try:
        mycursor.execute("INSERT INTO ITEM_CATALOG(Name) VALUES (%s)", (name,))
        #db.commit()
        # print("here")
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New catalog created successfully.")

    mycursor.execute("UPDATE USERS SET Creator_Flag = 1 WHERE User_ID = (%s)", (id,))

def createInventory(id: int):
    found = 0
    while found == 0:
        catalog = input("Which item catalog would you like to create an inventory for.")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
        
    name = input("What would you like the name of your inventory to be?")
    try:
        mycursor.exectute("INSERT INTO INVENTORY(Name) VALUES (%s)", (name,))
        #db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New inventory created successfully.")

    mycursor.execute("UPDATE USERS SET Player_Flag = 1 WHERE User_ID = (%s)", (id,))

def createItem(id: int): #Implement last 4 flag constraints found in phase 3 doc TODO
    found = 0
    while found == 0:
        catalog = input("Which item catalog would you like to create an item for.")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * CREATOR_EDIT_CATALOG WHERE (Creator_ID,Catalog_ID) = (%s,%s)", (id, mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that catalog")
                found = 0

    
    found = 0
    while found == 0:
        name = input("What would you like the name of your item to be?")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (name))
        for x in mycursor:
            found += 1
        if found != 0:
            print("That item already exists. Please enter a valid item name.")
            found = 0
        else:
            found = 1
    
    rarity = input("What is the rarity of your item?")
    number = input("What is the total quantity of the item?")
    desc = input("What is the description of your item?")
    cat = input("Does your item have a category? If none, put 0.")
    if cat == "0":
        cat = None
    weight = input("What is your items weight in kilograms? Please enter up to 2 decimal places.")
    weight = round(weight,2)
    resource = input("Is your item a resource? Put 0 if false, and 1 if true.")
    if resource == "1":
        resource = True
    else:
        resource = False
    weaparm = input("Is your item a weapon or armor? Put 0 if false, and 1 if true.")
    if weaparm == "1":
        weaparm = True
    else:
        weaparm = False
    consumable = input("Is your item a consumable? Put 0 if false, and 1 if true.")
    if consumable == "1":
        consumable = True
    else:
        consumable = False
    upgrade = input("Is your item an upgradable item? Put 0 if false, and 1 if true.")
    if upgrade == "1":
        upgrade = True
    else:
        upgrade = False
    try:
        mycursor.exectute("INSERT INTO ITEM(Weight, Overall_Quan,Description,Category,Rarity,Name,C_Flag,R_Flag,WA_Flag,UI_Flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (weight,number,desc,cat,rarity,name,consumable,resource,weaparm,upgrade))
        #db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New item created successfully.")

def modifyItem(id: int):
    found = 0
    catalogID = 0
    while found == 0:
        catalog = input("Which item catalog would you like to modify an item for.")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * CREATOR_EDIT_CATALOG WHERE (Creator_ID,Catalog_ID) = (%s,%s)", (id, mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that catalog")
                found = 0
        catalogID = mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
    
    found = 0
    itemID = 0
    while found == 0:
        item = input("Which item would you like to modify?")
        mycursor.execute("SELECT * FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item,catalogID))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item does not exist in this catalog. Please enter a valid item.")

    itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item,catalogID))
    choice = -1
    while choice != 0:
        print("What would you like to modify?")
        print("1. Name\t\t\t2. Description\t\t\t3. Rarity")
        print("4. Weight\t\t\t5. Quantity\t\t\t6. Category")
        print("7. Weapon/Armor Status\t\t\t8. Craftable Status")
        print("9. Resource Status\t\t\t10. Consumable Status")
        print("0. Quit")
        choice = int(input(""))
        while choice < 0 or choice > 10:
                print("Invalid action, please choose from the menu.")
                confirm = input("press enter")
        match choice:
            case 1:
                update = input("What would you like the new name to be?")
                mycursor.execute("UPDATE ITEM SET Name = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 2:
                update = input("What would you like the new description to be?")
                mycursor.execute("UPDATE ITEM SET Description = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 3:
                update = input("What would you like the new rarity to be?")
                mycursor.execute("UPDATE ITEM SET Rarity = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 4:
                update = input("What would you like the new weight to be?")
                update = round(update, 2)
                mycursor.execute("UPDATE ITEM SET Weight = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 5:
                update = input("What would you like the new quantity to be?")
                mycursor.execute("UPDATE ITEM SET Overall_Quan = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 6:
                update = input("What would you like the new category to be?")
                mycursor.execute("UPDATE ITEM SET Category = (%s) WHERE Item_ID = (%s)", (update,itemID))
            case 7:
                update = input("Would you like the item to be a weapon or armor (1 for yes, 0 for no)?")
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET WA_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID))
                else:
                    print("Invalid input")
            case 8:
                update = input("Would you like the item to be craftable (1 for yes, 0 for no)?")
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET C_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID))
                else:
                    print("Invalid input")
            case 9:
                update = input("Would you like the item to be a resource (1 for yes, 0 for no)?")
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET R_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID))
                else:
                    print("Invalid input")
            case 10:
                update = input("Would you like the item to be upgradable (1 for yes, 0 for no)?")
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET UI_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID))
                else:
                    print("Invalid input")
            case 0:
                quit()

    pass

def giveInventoryAccess(id: int):
    found = 0
    invenID = 0
    inventory = 0
    while found == 0:
        inventory = input("Which inventory would you like to give another user access to.")
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (inventory,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * USER_EDIT_INVENTORY WHERE (Creator_ID,Inventory_ID) = (%s,%s)", (id, mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that inventory")
                found = 0
        invenID = mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))

    found = 0
    userID = 0
    while found == 0:
        user = input("Which user would you like to give access to this inventory?")
        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s)", (user,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That user does not exist, Please enter a valid user.")
        userID = mycursor.execute("SELECT User_ID FROM USERS WHERE Name = (%s)", (user,))

    catalog = mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))

    try:
        mycursor.exectute("INSERT INTO USER_EDIT_INVENTORY(User_ID,Catalog_ID,Inventory_ID) VALUES (%s,%s,%s)", (userID,catalog,invenID))
        #db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    
    mycursor.execute("UPDATE USERS SET Player_Flag = 1 WHERE User_ID = (%s)", (userID,))

    print("Access updated successfully.")

def giveCatalogAccess(id: int):
    found = 0
    catalogID = 0
    while found == 0:
        catalog = input("Which item catalog would you like to give another user access to.")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * CREATOR_EDIT_CATALOG WHERE (Creator_ID,Catalog_ID) = (%s,%s)", (id, mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that catalog")
                found = 0
        catalogID = mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))

    found = 0
    userID = 0
    while found == 0:
        user = input("Which user would you like to give access to this catalog?")
        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s)", (user,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That user does not exist, Please enter a valid user.")
        userID = mycursor.execute("SELECT User_ID FROM USERS WHERE Name = (%s)", (user,))

    try:
        mycursor.exectute("INSERT INTO CREATOR_EDIT_CATALOG(User_ID,Catalog_ID) VALUES (%s)", (userID,catalogID))
        #db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    
    mycursor.execute("UPDATE USERS SET Creator_Flag = 1 WHERE User_ID = (%s)", (userID,))

    print("Access updated successfully.")

def equipItem(id: int):
    found = 0
    invenID = 0
    inventory
    while found == 0:
        inventory = input("Which inventory would you like to equip an item from.")
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (inventory,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * USER_EDIT_INVENTORY WHERE (Creator_ID,Inventory_ID) = (%s,%s)", (id, mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that inventory")
                found = 0
        invenID = mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))
    
    catalog = mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))

    found = 0
    itemID = 0
    while found == 0:
        item = input("Which item would you like to equip?")
        mycursor.execute("SELECT * FROM CONTAINS_ITEM WHERE (Name,Inventory_ID) = (%s,%s)", (item,mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (invenID,))))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item does not exist in this inventory. Please enter a valid item.")
        
        check = mycursor.execute("SELECT WA_Flag FROM ITEM WHERE Name = (%s)", (item,))
        if check != 1:
            print("This item is not equipable. Please enter an equipable item.")
            found = 0
        itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE Name = (%s)", (item,))
    
    try:
        mycursor.execute("INSERT INTO WEAPON_ARMOR_EQUIPPED(Item_ID,Catalog_ID,Inventory_ID) VALUES (%s,%s,%s)", (itemID,catalog,invenID))
        #db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))

    print("Item equipped successfully")

def searchCatalog(id: int):
    found = 0
    catalogID = 0
    while found == 0:
        catalog = input("What is the name of the Catalog you would like to search?")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That catalog does not exist. Please enter a valid catalog.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE(Creator_ID,Catalog_ID) = (%s,%s)", (id,mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (catalog,))))
            for x in mycursor:
                newFound += 1
            mycursor.execute("SELECT * FROM USER_EDIT_INVENTORY WHERE(User_ID,Catalog_ID) = (%s,%s)", (id,mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (catalog,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have access to this Catalog. Please enter a catalog you have access to.")
                found = 0
            catalogID = mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (catalog,))
    
    found = 0
    item = input("What is the item you are searching for?")
    mycursor.execute("SELECT * FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item, catalogID))
    for x in mycursor:
        found += 1
    if found == 0:
        print("The item was not found in this catalog.")
    else:
        itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item,catalogID))
        af.printItemInfo(itemID)
    pass

def searchInventory(id: int):
    found = 0
    invenID = 0
    inventory = 0
    while found == 0:
        inventory = input("Which inventory would you like to search.")
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (inventory,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * USER_EDIT_INVENTORY WHERE (User_ID,Inventory_ID) = (%s,%s)", (id, mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that inventory")
                found = 0
        invenID = mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))

    found = 0
    item = input("What is the item you are searching for?")
    mycursor.execute("SELECT * FROM CONTAINS_ITEM WHERE (Name,Inventory_ID) = (%s,%s)", (item, invenID))
    for x in mycursor:
        found += 1
    if found == 0:
        print("The item was not found in this inventory.")
    else:
        itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE (Name,Inventory_ID) = (%s,%s)", (item,invenID))
        af.printItemInfo(itemID)

    pass

def searchSystem(id: int):
    found = 0
    while found == 0:
        name = input("What is the name of the inventory or catalog you would like to search for?")
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (name,))
        for x in mycursor:
            invenInfo = mycursor.fetchall()
            catID,invenID,invenName = invenInfo
            print(f"Catalog ID: {catID}, Inventory ID: {invenID}, Name: {invenName}")
            found += 1
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (name,))
        for x in mycursor:
            catInfo = mycursor.fetchall()
            userID,catalogID,catName = catInfo
            print(f"User ID: {userID}, Catalog ID: {catalogID}, Name: {catName}")
            found += 1
        if found == 0:
            print("Name of Inventory or Catalog not found, please input a valid Inventory or Catalog name")
    pass

def sortCatalog(id: int):
    pass

def sortInventory(id: int):
    pass

def deleteCatalog(id: int):
    pass

def deleteInventory(id: int):
    pass

def deleteItem(id: int):
    pass

def updateInventory(id: int):
    found = 0
    invenID = 0
    inventory = 0
    while found == 0:
        inventory = input("Which inventory would you like to update.")
        mycursor.execute("SELECT * FROM INVENTORY WHERE Name = (%s)", (inventory,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That inventory does not exist. Please enter a valid inventory.")
        if found != 0:
            newFound = 0
            mycursor.execute("SELECT * USER_EDIT_INVENTORY WHERE (User_ID,Inventory_ID) = (%s,%s)", (id, mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that inventory")
                found = 0
        invenID = mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))

    found = 0
    itemID = 0
    while found == 0:
        item = input("Which item would you like to update?")
        mycursor.execute("SELECT * FROM CONTAINS_ITEM WHERE (Name,Inventory_ID) = (%s,%s)", (item, invenID))
        for x in mycursor:
            found += 1
        if found == 0:
            print("The item was not found in this inventory.")
        else:
            itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE (Name,Inventory_ID) = (%s,%s)", (item,invenID))
    
    choice = input("Would you like to add or remove items from your inventory? (Add = 1, Remove = 0)")
    if choice == 1:
        add = int(input("How much of the item would you like to add?"))
        if add <= af.checkQuanity(id):
            mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (add,itemID,invenID))
    if choice == 0:
        remove = int(input("How much of the item would you like to add?"))
        if remove <= mycursor.execute("SELECT Quantity FROM CONTAINS_ITEM WHERE Item_ID = (%s)", (itemID,)):
            mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (remove,itemID,invenID))
    pass



def craftItem(id: int):
    pass


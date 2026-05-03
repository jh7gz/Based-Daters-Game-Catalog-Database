import mysql.connector
import aggregationFunctions as af
from enum import Enum

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = db.cursor(buffered=True)

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

                if psswrd == '0'or first == '0' or last == '0' or middle == '0':
                    quit()

                try:
                    mycursor.execute("INSERT INTO USERS(Profile_Name,Password,F_name,M_Init,L_Name) VALUES (%s,%s,%s,%s,%s)", (id,psswrd,first,middle,last))
                    db.commit()
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
                print("New account created, proceeding to login")

            if found != 0:
                print("That Profile Name is in use, please try again")
                id = '1'
                found = 0


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
        mycursor.execute("SELECT User_ID FROM USERS WHERE Profile_Name = (%s) AND Password = (%s)", (id, pswd))
        for x in mycursor:
            correct += 1
            userid = x[0]
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
        if name == "0":
            return
        if name == "":
            print("That item catalog already exists. Please enter a valid new catalog name.")
       
    try:
        mycursor.execute("INSERT INTO ITEM_CATALOG(Name) VALUES (%s)", (name,))
        
        # print("here")
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New catalog created successfully.")

    mycursor.execute("UPDATE USERS SET Creator_Flag = 1 WHERE User_ID = (%s)", (id,))

    # db.commit()

    mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE NAME = (%s)", (name,))
    catalogID = mycursor.fetchone()[0]
    mycursor.execute("INSERT INTO CREATOR_EDIT_CATALOG(Creator_ID, Catalog_ID) VALUES (%s, %s)", (id, catalogID,))

    db.commit()

def createInventory(id: int):
    found = 0
    catalogID = 0
    while found == 0:
        print("Here are your options:")
        mycursor.execute("SELECT Name FROM ITEM_CATALOG")
        for x in mycursor:
            for y in x:
                print(y)
        catalog = input("Which item catalog would you like to create an inventory for.")
        if catalog == '0':
            return
        
        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        
        for x in mycursor:
            found += 1
            catalogID = x[0]

        if found == 0:
            print("That item catalog does not exist. Please enter a valid catalog.")
        # catalogID = mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        # print(catalogID)
        
    name = input("What would you like the name of your inventory to be?")

    if name == '0':
        return
    
    try:
        mycursor.execute("INSERT INTO INVENTORY(Name, Catalog_ID) VALUES (%s,%s)", (name, catalogID))
        
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New inventory created successfully.")

    mycursor.execute("UPDATE USERS SET Player_Flag = 1 WHERE User_ID = (%s)", (id,))

    db.commit()

def createItem(id: int): #Implement last 4 flag constraints found in phase 3 doc TODO
    found = 0
    while found == 0:
        catalog = input("Which item catalog would you like to create an item for.")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catalog does not exist. Please enter a valid catalog.")
        if found != 0:
            newFound = 0

            mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
            catalogID = mycursor.fetchone()[0]

            mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE (Creator_ID,Catalog_ID) = (%s,%s)", (id, catalogID, ))
            for x in mycursor:
                newFound += 1
            if newFound == 0:
                print("You do not have edit access for that catalog")
                found = 0

    
    found = 0
    while found == 0:
        name = input("What would you like the name of your item to be?")
        mycursor.execute("SELECT * FROM ITEM_CATALOG WHERE Name = (%s)", (name,))
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
    weight = float(weight)
    weight = round(weight,2)
    resource = input("Is your item a resource? Put 0 if false, and 1 if true.")
    if resource == "1":
        resource = True
    else:
        resource = False
    consumable = "0"
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
        mycursor.execute("INSERT INTO ITEM(Catalog_ID,Weight, Overall_Quan,Description,Category,Rarity,Name,C_Flag,R_Flag,WA_Flag,UI_Flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (catalogID,weight,number,desc,cat,rarity,name,consumable,resource,weaparm,upgrade,))
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))

    #set item effects
    another = 'y'
    
    while (weaparm == 1 or consumable == 1) and another == 'y':
        effect = input("What is the effect your item has? ")
        constInc = input("What is the numerical modifier of your effect? ")
        if constInc == '': constInc = 0
        else: 
            try: constInc = int(constInc)
            except: 
                print("Invalid number") 
                continue
        percentInc = input("What is the percent modifier of your effect? ")
        if percentInc == '': percentInc = 0
        else: 
            try: percentInc = int(percentInc)
            except: 
                print("Invalid percent") 
                continue
        duration = input("What is the duration of your effect? ")
        if duration == '': duration = 0
        else: 
            try: duration = int(duration)
            except: 
                print("Invalid duration") 
                continue


        mycursor.execute("SELECT Item_ID FROM ITEM WHERE NAME = (%s)", (name,))
        itemID = mycursor.fetchone()[0]

        mycursor.execute("INSERT INTO ITEM_EFFECT(Item_ID, Catalog_ID, Effect, Constant_Inc, Percent_Inc, Duration) VALUES (%s, %s, %s, %s, %s, %s)", (itemID, catalogID, effect, constInc, percentInc, duration))


        another = input("would you like to add another effect?(y/n) ")

    print("Item created successfully.")

    db.commit()


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
        mycursor.execute("INSERT INTO USER_EDIT_INVENTORY(User_ID,Catalog_ID,Inventory_ID) VALUES (%s,%s,%s)", (userID,catalog,invenID))
        db.commit()
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
        mycursor.execute("INSERT INTO CREATOR_EDIT_CATALOG(User_ID,Catalog_ID) VALUES (%s)", (userID,catalogID))
        db.commit()
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
        db.commit()
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
    if mycursor.execute("SELECT Creator_Flag FROM USERS WHERE User_ID = (%s)",(id,)) == 1:    
        choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
        while choice != 0:
            if choice == 1:
                mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE Creator_ID = (%s) ORDER BY Name",(id,))
                for x in mycursor:
                    print(x)
            if choice == 2:
                mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE Creator_ID = (%s) ORDER BY Name DESC",(id,))
                for x in mycursor:
                    print(x)
            else:
                print("Invalid option, please try again.")
                choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
    pass

def sortInventory(id: int):
    if mycursor.execute("SELECT Player_Flag FROM USERS WHERE User_ID = (%s)",(id,)) == 1:    
        choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
        while choice != 0:
            if choice == 1:
                mycursor.execute("SELECT * FROM USER_EDIT_INVENTORY WHERE User_ID = (%s) ORDER BY Name",(id,))
                for x in mycursor:
                    print(x)
            if choice == 2:
                mycursor.execute("SELECT * FROM USER_EDIT_INVENTORY WHERE User_ID = (%s) ORDER BY Name DESC",(id,))
                for x in mycursor:
                    print(x)
            else:
                print("Invalid option, please try again.")
                choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
    pass

def deleteCatalog(id: int):
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

    choice = "no"
    while choice != "yes" or choice != "Yes":
        choice = input("Are you sure you would like to delete this catalog?")
    mycursor.execute("DELETE FROM ITEM_CATALOG WHERE Catalog_ID = (%s)", (catalogID,))
    pass

def deleteInventory(id: int):
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
    
    choice = "no"
    while choice != "yes" or choice != "Yes":
        choice = input("Are you sure you would like to delete this catalog?")
    mycursor.execute("DELETE FROM INVENTORY WHERE Inventory_ID = (%s)", (invenID,))
    pass

def deleteItem(id: int):
    found = 0
    catalogID = 0
    while found == 0:
        catalog = input("Which item catalog would you like to delete an item from.")
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
        item = input("Which item would you like to delete?")
        mycursor.execute("SELECT * FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item,catalogID))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item does not exist in this catalog. Please enter a valid item.")
        itemID = mycursor.execute("SELECT Item_ID FROM ITEM WHERE (Name,Catalog_ID) = (%s,%s)", (item,catalogID))

    choice = "no"
    while choice != "yes" or choice != "Yes":
        choice = input("Are you sure you would like to delete this item?")
    mycursor.execute("DELETE FROM ITEM WHERE Catalog_ID = (%s)", (itemID,))
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
    
    choice = 1
    while choice != 0:
        choice = input("Would you like to add or remove the item from your inventory? (Add = 1, Remove = 2, Quit = 0)")
        if choice == 1:
            add = int(input("How much of the item would you like to add?"))
            if add <= af.checkQuanity(id):
                mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (add,itemID,invenID))
            else:
                print ("There is not enough of this item to add to your inventory, please enter a valid number")
        if choice == 2:
            remove = int(input("How much of the item would you like to add?"))
            if remove <= mycursor.execute("SELECT Quantity FROM CONTAINS_ITEM WHERE Item_ID = (%s)", (itemID,)):
                mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (remove,itemID,invenID))
            else:
                print("You are trying to remove too much of the item from your inventory, please try again.")
        else:
            print("Invalid option, please try again.")
        
    pass

def viewCatalog():
    mycursor.execute("SELECT * FROM ITEM_CATALOG")
    for x in mycursor:
        print (x)
    pass

def viewInventory():
    mycursor.execute("SELECT * FROM INVENTORY")
    for x in mycursor:
        print (x)
    pass

def viewItem():
    mycursor.execute("SELECT * FROM ITEM")
    for x in mycursor:
        print (x)
    pass

def craftItem(id: int):
    pass


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
                email = input("Please enter your email.")
                
                while len(middle) > 1:

                    middle = input("Please input only middle initial: ")

                if psswrd == '0'or first == '0' or last == '0' or middle == '0' or email == "0":
                    quit()

                try:
                    #mycursor.execute("SELECT MAX(User_ID) FROM USERS")
                    #thisID = mycursor.fetchone()[0] + 1
                    mycursor.execute("INSERT INTO USERS(Profile_Name,Password,F_name,M_Init,L_Name) VALUES (%s,%s,%s,%s,%s)", (id,psswrd,first,middle,last))
                    db.commit()
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
                try:
                    mycursor.execute("SELECT User_ID FROM USERS WHERE Profile_Name = (%s)", (id,))
                    thisID = mycursor.fetchone()[0]
                    mycursor.execute("INSERT INTO USER_EMAIL(User_ID,email) VALUES (%s,%s)",(thisID,email))
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

    mycursor.execute("select inventory_id from inventory where (catalog_id, name) = (%s,%s)", (catalogID, name))
    invenID = mycursor.fetchone()[0]

    mycursor.execute("Insert into user_edit_inventory(user_id, catalog_id, inventory_id) values (%s, %s, %s)", (id, catalogID, invenID))

    db.commit()

#TODO add ranges and types

def createItem(id: int): 
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
    try: int(number)
    except: number = 1
    desc = input("What is the description of your item?")
    cat = input("Does your item have a category? If none, put 0.")
    if cat == "0" or cat == '':
        cat = None
    weight = input("What is your items weight in kilograms? Please enter up to 2 decimal places.")
    try: weight = float(weight)
    except: weight = float(1)
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
        print("This item will automatically not be a consumable, because weapons/armor cannot also be consumables.")
        consumable = False
    else:
        weaparm = False
        consumable = input("Is your item a consumable? Put 0 if false, and 1 if true.")
        if consumable == "1":
            consumable = True
        else:
            consumable = False
    if weaparm == True and resource == True:
        upgrade = input("Is your item an upgradable item? Put 0 if false, and 1 if true.")
    else:
        print("Item cannot be upgradable if it is not a weapon and a resource.")
        upgrade = False
    if upgrade == "1":
        upgrade = True
    else:
        upgrade = False

    # print(catalogID,weight,number,desc,cat,rarity,name,consumable,resource,weaparm,upgrade)
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

    #item ranges
    another = 'y'
    
    while weaparm == 1 and another == 'y':
        range = input("What is the range of your item? ")
        try: int(range)
        except: range = 0
        damage = input("What is damage at that range? ")
        try: int(damage)
        except: damage = 0

        mycursor.execute("INSERT INTO item_weapon_armor_range(Item_ID, Catalog_ID, warange, damage) VALUES (%s, %s, %s, %s)", (itemID, catalogID, range, damage,))

        another = input("would you like to add another range?(y/n) ")
    
    another = 'y'

    while weaparm == 1 and another == 'y':
        watype = input("What is the type of your item? ")

        mycursor.execute("INSERT INTO item_weapon_armor_type(Item_ID, Catalog_ID, watype) VALUES (%s, %s, %s)", (itemID, catalogID, watype,))

        another = input("would you like to add another type?(y/n) ")

    print("Item created successfully.")

    db.commit()

def updateUser(id:int):
    choice = -1
    while choice != 0:
        print("1. Profile Name\t\t\t2. Password")
        print("3. First name\t\t\t4. Last name")
        print("5. Middle Initial\t\t\t6. Add an Email")
        print("7. Remove an Email\t\t\t8. Modify an Email")
        print("0. Quit")
        choice = int(input("What would you like to modify?"))
        match choice:
            case 1:
                alter = input("What would you like to update your Profile name to?")
                mycursor.execute("UPDATE USERS SET Profile_Name = (%s) WHERE User_ID = (%s)",(alter,id))
            case 2:
                alter = input("What would you like to update your Password to?")
                mycursor.execute("UPDATE USERS SET Password = (%s) WHERE User_ID = (%s)",(alter,id))
            case 3:
                alter = input("What would you like to update your First name to?")
                mycursor.execute("UPDATE USERS SET F_Name = (%s) WHERE User_ID = (%s)",(alter,id))
            case 4:
                alter = input("What would you like to update your Last name to?")
                mycursor.execute("UPDATE USERS SET L_Name = (%s) WHERE User_ID = (%s)",(alter,id))
            case 5:
                alter = input("What would you like to update your Middle initial to?")
                while len(alter) > 1:
                    alter = input("Please input only middle initial: ")
                mycursor.execute("UPDATE USERS SET M_Init = (%s) WHERE User_ID = (%s)",(alter,id))
            case 6:
                alter = input("Which email would you like to add?")
                try:
                    mycursor.execute("INSERT INTO USER_EMAIL(User_ID,email) VALUES (%s,%s)",(id,alter))
                    db.commit()
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
                print("Email added successfully")
            case 7:
                mycursor.execute("SELECT * FROM USER_EMAIL WHERE User_ID = (%s)",(id,))
                count = 0
                for x in mycursor:
                    count += 1
                if count <= 1:
                    print("You only have 1 email and may not have less than 1 email.")
                else:
                    found = 0
                email = 0
                while found == 0:
                    print("Here are your options:")
                    mycursor.execute("SELECT Email FROM USER_EMAIL WHERE User_ID = (%s)",(id,))
                    for x in mycursor:
                        for y in x:
                            print(y)
                    email = input("Which email would you like to delete.")
                    if email == '0':
                        break
                    
                    mycursor.execute("SELECT Email FROM USER_EMAIL WHERE Email = (%s)", (email,))
                    
                    for x in mycursor:
                        found += 1

                    if found == 0:
                        print("That email does not exist. Please enter a valid email.")
                mycursor.execute("delete from USER_EMAIL where email = (%s)", (email,))
                
                print("Email updated successfully")
            case 8:
                found = 0
                email = 0
                while found == 0:
                    print("Here are your options:")
                    mycursor.execute("SELECT Email FROM USER_EMAIL WHERE User_ID = (%s)",(id,))
                    for x in mycursor:
                        for y in x:
                            print(y)
                    email = input("Which email would you like to modify.")
                    if email == '0':
                        break
                    
                    mycursor.execute("SELECT Email FROM USER_EMAIL WHERE Email = (%s)", (email,))
                    
                    for x in mycursor:
                        found += 1

                    if found == 0:
                        print("That email does not exist. Please enter a valid email.")
                newEmail = input("What would you like the new email to be")
                mycursor.execute("UPDATE USER_EMAIL SET Email = (%s) WHERE Email = (%s)",(newEmail,email))
                print("Email updated successfully")

    pass

def updateCatalog(id: int):

    while True:
        catalog = input("Which catalog would you like to update? ")
        if catalog == '0':
            return

        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        try: catalogID = mycursor.fetchone()[0]
        except: 
            print("No such catalog exists! ")
            continue
        break


    newName = input("What would you like to rename the catalog to? ")

    mycursor.execute("UPDATE Item_catalog set name = (%s) where catalog_id = (%s)", (newName, catalogID,))

    print("Catalog successfully updated")
    db.commit()

def modifyInventory(id):
    
    while True:
        inven = input("Which inventory would you like to update? ")
        if inven == '0':
            return

        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue
        break


    newName = input("What would you like to rename the inventory to? ")

    mycursor.execute("UPDATE INVENTORY set name = (%s) where inventory_id = (%s)", (newName, invenID,))

    print("Inventory successfully updated")
    db.commit()

def modifyItem(id: int):

    while True:
        catalog = input("Which item catalog would you like to modify an item for? ")
        if catalog == '0':
            return

        mycursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        try: catalogID = mycursor.fetchone()[0]
        except: 
            print("No such catalog exists! ")
            continue

        mycursor.execute("SELECT * from CREATOR_EDIT_CATALOG WHERE (Creator_ID,Catalog_ID) = (%s,%s)", (id, catalogID,))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to that catalog! ")
            continue

        break

    while True:
        item = input("Which item would you like to modify? ")
        if item == '0':
            return

        mycursor.execute("SELECT item_id FROM ITEM WHERE (name,catalog_id) = (%s,%s)", (item,catalogID,))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue
        break
    
    choice = -1
    while choice != 0:
        print("What would you like to modify?")
        print("1. Name\t\t\t2. Description\t\t\t3. Rarity")
        print("4. Weight\t\t\t5. Quantity\t\t\t6. Category")
        print("7. Weapon/Armor Status\t\t\t 8.Type" )
        print("9. Resource Status\t\t\t10. Consumable Status")
        print("11. Effects\t\t\t12. Ranges/Damage")
        print("0. Quit")

        

        while choice < 0 or choice > 13:
                try: 
                    choice = int(input(""))
                except: 
                    choice = -1
                    print("Invalid action, please choose from the menu.")
                    continue
        
        match choice:
            case 1:
                update = input("What would you like the new name to be?")
                mycursor.execute("UPDATE ITEM SET Name = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 2:
                update = input("What would you like the new description to be?")
                mycursor.execute("UPDATE ITEM SET Description = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 3:
                update = input("What would you like the new rarity to be?")
                mycursor.execute("UPDATE ITEM SET Rarity = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 4:
                update = input("What would you like the new weight to be?")
                update = round(update, 2)
                mycursor.execute("UPDATE ITEM SET Weight = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 5:
                update = input("What would you like the new quantity to be?")
                mycursor.execute("UPDATE ITEM SET Overall_Quan = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 6:
                update = input("What would you like the new category to be?")
                mycursor.execute("UPDATE ITEM SET Category = (%s) WHERE Item_ID = (%s)", (update,itemID,))
            case 7:
                flag = True
                while flag:
                    update = input("Would you like the item to be a weapon or armor (1 for yes, 0 for no)?")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False
                                   
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET WA_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID,))
                else:
                    print("Invalid input")
            case 9:
                flag = True
                while flag:
                    update = input("Would you like the item to be a resource (1 for yes, 0 for no)?")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET R_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID,))
                else:
                    print("Invalid input")
            case 10:
                flag = True
                while flag:
                    update = input("Would you like the item to be upgradable (1 for yes, 0 for no)?")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False
                if update == 0 or update == 1:
                    mycursor.execute("UPDATE ITEM SET UI_Flag = (%s) WHERE Item_ID = (%s)", (update,itemID,))
                else:
                    print("Invalid input")

            case 11:
                flag = True
                while flag:
                    update = input("Would you like to add(1) or delete(2) an effect? ")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False

                if update == 0:
                    break
                else:

                    if update == 2:
                        print("Current Effects:")
                        mycursor.execute("Select effect, constant_inc, percent_inc, duration from item_effect where item_id = (%s)", (itemID,))
                        for x in mycursor.fetchall():
                            effect, constantInc, percentInc, duration = x
                            print(f"Item ID: {itemID}, Effect: {effect}, Constant Increase: {constantInc}, Percent Increase: {percentInc}, Duration: {duration}")
                        flag = True
                        while flag:
                            effectName = input("\n Which effect would you like to delete?(Input effect name): ")
                            mycursor.execute("Select * from item_effect where effect = (%s)", (effectName,))
                            try: mycursor.fetchone()[0]
                            except: 
                                print("Input valid effect name!")
                                continue
                            flag = False
                        mycursor.execute("delete from item_effect where effect = (%s)", (effectName,))
                        print("Effect deleted successfully!")

                    else:
                        mycursor.execute("select c_flag, wa_flag from item where item_id = (%s)", (itemID,))
                        consumable, weaparm = mycursor.fetchall()[0]

                    
                        if consumable == 0 and weaparm == 0:
                            print("Cannot edit effects if item is neither a weapon nor consumable! ")
                            break
                            
                                                    
                        else:
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

                            mycursor.execute("INSERT INTO ITEM_EFFECT(Item_ID, Catalog_ID, Effect, Constant_Inc, Percent_Inc, Duration) VALUES (%s, %s, %s, %s, %s, %s)", (itemID, catalogID, effect, constInc, percentInc, duration))

            case 12:
                #item ranges

                mycursor.execute("select wa_flag from item where item_id = (%s)", (itemID,))
                weaparm = mycursor.fetchone()[0]

                if weaparm != 1:
                    print("Items cannot have ranges and damage if they aren't a weapon/armor! ")
                    break

                flag = True
                while flag:
                    update = input("Would you like to add(1) or delete(2) a range? ")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False

                if update == 0:
                    break
                else:
                    if update == 1:

                        range = input("What is the range of your item? ")
                        try: int(range)
                        except: range = 0
                        damage = input("What is damage at that range? ")
                        try: int(damage)
                        except: damage = 0

                        mycursor.execute("INSERT INTO item_weapon_armor_range(Item_ID, Catalog_ID, warange, damage) VALUES (%s, %s, %s, %s)", (itemID, catalogID, range, damage,))

                    else:
                        print("Current Ranges:")
                        mycursor.execute("Select warange, damage  from item_weapon_armor_range where item_id = (%s)", (itemID,))
                        for x in mycursor.fetchall():
                            range, damage = x
                            print(f"Item ID: {itemID}, Range: {range}, Damage: {damage}")
                        flag = True
                        while flag:
                            range = input("\n Which effect would you like to delete?(Input range): ")
                            mycursor.execute("Select * from item_weapon_armor_range where warange = (%s)", (range,))
                            try: mycursor.fetchone()[0]
                            except: 
                                print("Input valid range!")
                                continue
                            flag = False
                        mycursor.execute("delete from item_weapon_armor_range where warange = (%s)", (range,))
                        print("Range deleted successfully!")



            case 8:
                #types
                mycursor.execute("select wa_flag from item where item_id = (%s)", (itemID,))
                weaparm = mycursor.fetchone()[0]

                if weaparm != 1:
                    print("Items cannot have types if they aren't a weapon/armor! ")
                    break

                flag = True
                while flag:
                    update = input("Would you like to add(1) or delete(2) a type? ")
                    try: update = int(update)
                    except: 
                        update = -1    
                    if update > 2 or update < 0:
                        print("Please enter a valid input. ")
                    else:                    
                        flag = False

                if update == 0:
                    break
                else:
                    if update == 1:

                        Type = input("What is the type of your item? ")
                        mycursor.execute("INSERT INTO item_weapon_armor_type(Item_ID, Catalog_ID, watype) VALUES (%s, %s, %s)", (itemID, catalogID, Type))

                    else:
                        print("Current Types:")
                        mycursor.execute("Select watype from item_weapon_armor_type where item_id = (%s)", (itemID,))
                        for x in mycursor.fetchall():
                            Type = x[0]
                            print(f"Item ID: {itemID}, Type: {Type}")
                        flag = True
                        while flag:
                            Type = input("\n Which type would you like to delete?(Input type): ")
                            mycursor.execute("Select * from item_weapon_armor_type where watype = (%s)", (Type,))
                            try: mycursor.fetchone()[0]
                            except: 
                                print("Input valid type!")
                                continue
                            flag = False
                        mycursor.execute("delete from item_weapon_armor_type where watype = (%s)", (Type,))
                        print("Type deleted successfully!")


            case 0:
                db.commit()
                return
        choice = -1



        print("Item modified successfully! ")
        db.commit()

def giveInventoryAccess(id: int):

    while True:
        inventory = input("Which inventory would you like to change access rights? ")
        if inventory == '0':
            return

        mycursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue
        
        mycursor.execute("SELECT * from USER_EDIT_INVENTORY WHERE (User_ID, Inventory_ID) = (%s,%s)", (id,invenID,))
        try: mycursor.fetchone()[0]
        except:
            print("You don't have edit access to that inventory!")
            continue
        break

    while True:
        user = input("Which user would you like to access this inventory? ")
        if user == '0':
            return

        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s)", (user,))
        try: otherUserID = mycursor.fetchone()[0]
        except: 
            print("No such user exists! ")
            continue
        break

    mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))
    catalog = mycursor.fetchone()[0]

    mycursor.execute("INSERT INTO USER_EDIT_INVENTORY(User_ID,Catalog_ID,Inventory_ID) VALUES (%s,%s,%s)", (otherUserID,catalog,invenID,))
    
    mycursor.execute("UPDATE USERS SET Player_Flag = 1 WHERE User_ID = (%s)", (otherUserID,))

    print("Access updated successfully.")
    db.commit()

def giveCatalogAccess(id: int):

    while True:
        catalog = input("Which catalog would you like to change access rights? ")
        if catalog == '0':
            return

        mycursor.execute("SELECT catalog_id FROM item_catalog WHERE Name = (%s)", (catalog,))
        try: catalogID = mycursor.fetchone()[0]
        except: 
            print("No such catalog exists! ")
            continue
        
        mycursor.execute("select * from creator_edit_catalog where (creator_id, catalog_id) = (%s,%s)", (id, catalogID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have edit access for that catalog! ")
            continue
        break

    while True:
        user = input("Which user would you like to access this catalog? ")
        if user == '0':
            return

        mycursor.execute("SELECT * FROM USERS WHERE Profile_Name = (%s)", (user,))
        try: otherUserID = mycursor.fetchone()[0]
        except: 
            print("No such user exists! ")
            continue
        break

    mycursor.execute("INSERT INTO CREATOR_EDIT_CATALOG(Creator_ID,Catalog_ID) VALUES (%s,%s)", (otherUserID,catalogID,))
    
    mycursor.execute("UPDATE USERS SET Creator_Flag = 1 WHERE User_ID = (%s)", (otherUserID,))

    print("Access updated successfully.")
    db.commit()

def equipItem(id: int):
 
    while True:
        inventory = input("Which inventory would you like to equip an item from? ")
        if inventory == '0':
            return

        mycursor.execute("SELECT inventory_id FROM inventory WHERE Name = (%s)", (inventory,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue
        
        mycursor.execute("SELECT * from USER_EDIT_INVENTORY WHERE (user_ID,Inventory_ID) = (%s,%s)", (id, invenID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have edit access for that inventory!")
            continue

        mycursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Name = (%s)", (inventory,))
        catalogID = mycursor.fetchone()[0]
        break
 
    while True:
        item = input("Which item would you like to equip? ")
        if item == '0':
            return

        mycursor.execute("SELECT item_id FROM item WHERE (name, catalog_id) = (%s,%s)", (item,catalogID,))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue
        
        mycursor.execute("SELECT * from item WHERE (item_ID, catalog_id, wa_flag) = (%s,%s,%s)", (itemID, catalogID,1))
        try: mycursor.fetchone()[0]
        except:
            print("That item is not equippable! ")
            continue

        break

    mycursor.execute("INSERT INTO WEAPON_ARMOR_EQUIPPED(Item_ID,Catalog_ID,Inventory_ID) VALUES (%s,%s,%s)", (itemID,catalogID,invenID))

    print("Item equipped successfully")
    db.commit()

def searchCatalog(id: int):

    while True:
        catalog = input("What is the name of the Catalog you would like to search? ")
        if catalog == '0':
            return

        mycursor.execute("SELECT catalog_id FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
        try: catalogID = mycursor.fetchone()[0]
        except: 
            print("No such catalog exists! ")
            continue
        
        mycursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG WHERE(Creator_ID,Catalog_ID) = (%s,%s)", (id,catalogID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to this catalog! ")
            continue

        break

    while True:
        item = input("What is the name of the item you are searching for? ")
        if item == '0':
            return

        mycursor.execute("SELECT item_id FROM item WHERE (Name,catalog_id) = (%s,%s)", (item,catalogID,))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue
        break

    af.printItemInfo(itemID)

def searchInventory(id: int):

    while True:
        inventory = input("What is the name of the inventory you would like to search? ")
        if inventory == '0':
            return

        mycursor.execute("SELECT inventory_id FROM inventory WHERE Name = (%s)", (inventory,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue
        
        mycursor.execute("SELECT * FROM user_edit_inventory WHERE(user_id,inventory_id) = (%s,%s)", (id,invenID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to this inventory! ")
            continue

        break
    mycursor.execute("select catalog_id from inventory where inventory_id = (%s)", (invenID,))
    catalogID = mycursor.fetchone()[0]

    while True:
        item = input("What is the name of the item you are searching for? ")
        if item == '0':
            return

        mycursor.execute("SELECT item_id FROM item WHERE (Name,catalog_id) = (%s,%s)", (item,catalogID,))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue
        break

    af.printItemInfo(itemID)

def searchSystem(id: int):

    while True:
        name = input("What is the name of the inventory or catalog you would like to search for? ")
        if name == '0':
            return

        mycursor.execute("SELECT * FROM inventory WHERE Name = (%s)", (name,))
        try: ID = mycursor.fetchone()[0]
        except: 
            mycursor.execute("SELECT * from item_catalog where Name = (%s)", (name,))
            try: ID = mycursor.fetchone()[0]
            except:
                print("There are no inventories or catalogs with that name! ")
                continue
            
        
        mycursor.execute("SELECT * FROM user_edit_inventory WHERE(user_id,inventory_id) = (%s,%s)", (id,ID))
        try: mycursor.fetchone()[0]
        except:
            mycursor.execute("SELECT * FROM creator_edit_catalog WHERE(creator_id,catalog_id) = (%s,%s)", (id,ID))
            try: mycursor.fetchone()[0]
            except:
                print("You do not have access to this inventory/catalog!")
                continue
        break
    
    mycursor.execute("Select * from inventory where inventory_id = (%s)", (ID,))
    try:
        invenID, catID, catName = mycursor.fetchall()[0]
        print(f"Inventory ID: {invenID}, Catalog ID: {catID}, Name: {catName}")
    except: 
        mycursor.execute("Select * from item_catalog where catalog_id = (%s)", (ID,))
        catalogID, name = mycursor.fetchall()[0]
        print(f"Catalog ID: {catalogID}, Name: {name}")
        
def sortCatalog(id: int):
    mycursor.execute("SELECT creator_flag FROM USERS WHERE User_ID = (%s)",(id,))
    flag = mycursor.fetchone()[0]
    if flag == 1:   
        choice = -1
        while choice != 0:

            try: choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
            except: choice = -1

            if choice == 1:
                mycursor.execute("SELECT Name FROM creator_edit_catalog JOIN item_catalog ON creator_edit_catalog.catalog_id = item_catalog.catalog_id WHERE creator_id = (%s) ORDER BY Name ASC",(id,))
                for x in mycursor:
                    print(x)
            elif choice == 2:
                mycursor.execute("SELECT Name FROM creator_edit_catalog JOIN item_catalog ON creator_edit_catalog.catalog_id = item_catalog.catalog_id WHERE creator_id = (%s) ORDER BY Name DESC",(id,))
                for x in mycursor:
                    print(x)
            elif choice == 0:
                return
            else:
                print("Invalid option, please try again.")

def sortInventory(id: int):

    mycursor.execute("SELECT Player_Flag FROM USERS WHERE User_ID = (%s)",(id,))
    flag = mycursor.fetchone()[0]
    if  flag == 1:    
        choice = -1
        while choice != 0:

            try: choice = int(input("Would you like to sort by name in Ascending (1) or Descending (2) order? Enter 0 to quit"))
            except: choice = -1

            if choice == 1:
                mycursor.execute("SELECT Name FROM USER_EDIT_INVENTORY JOIN INVENTORY ON USER_EDIT_INVENTORY.Inventory_ID = INVENTORY.Inventory_ID WHERE User_ID = (%s) ORDER BY Name ASC",(id,))
                for x in mycursor:
                    print(x)
            elif choice == 2:
                mycursor.execute("SELECT Name FROM USER_EDIT_INVENTORY JOIN INVENTORY ON USER_EDIT_INVENTORY.Inventory_ID = INVENTORY.Inventory_ID WHERE User_ID = (%s) ORDER BY Name DESC",(id,))
                for x in mycursor:
                    print(x)
            elif choice == 0:
                return
            else:
                print("Invalid option, please try again.")
    
def deleteCatalog(id: int):

    while True:
        catalog = input("What is the name of the catalog you would like to delete? ")
        if catalog == '0':
            return

        mycursor.execute("SELECT catalog_id FROM item_catalog WHERE Name = (%s)", (catalog,))
        try: catalogID = mycursor.fetchone()[0]
        except: 
            print("No such catalog exists! ")
            continue
        
        mycursor.execute("SELECT * FROM creator_edit_catalog WHERE (creator_id, catalog_id) = (%s, %s)", (id,catalogID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to this catalog! ")
            continue
        break

    confirm = input("Are you sure you wish to delete this catalog?(y/n) \n")
    if confirm == 'y':
        print("Catalog deleted!")
        mycursor.execute("delete from item_catalog where catalog_id = (%s)", (catalogID,))
        return
    else:
        print("Catalog NOT deleted!")
        return

def deleteInventory(id: int):

    while True:
        inventory = input("What is the name of the inventory you would like to delete? ")
        if inventory == '0':
            return

        mycursor.execute("SELECT inventory_id FROM inventory WHERE Name = (%s)", (inventory,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue
        
        mycursor.execute("SELECT * FROM user_edit_inventory WHERE (user_id, inventory_id) = (%s, %s)", (id,invenID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to this inventory! ")
            continue
        break

    confirm = input("Are you sure you wish to delete this inventory?(y/n) \n")
    if confirm == 'y':
        print("Inventory deleted!")
        mycursor.execute("delete from inventory where inventory_id = (%s)", (invenID,))
        return
    else:
        print("Inventory NOT deleted!")
        return

def deleteItem(id: int):
    
    while True:
        item = input("What is the name of the item you would like to delete? ")
        if item == '0':
            return

        mycursor.execute("SELECT item_id FROM item WHERE Name = (%s)", (item,))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue

        mycursor.execute("select catalog_id from item where item_ID = (%s)", (itemID,))
        catalogID = mycursor.fetchone()[0]
        
        mycursor.execute("SELECT * FROM creator_edit_catalog WHERE (creator_id, catalog_id) = (%s, %s)", (id,catalogID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have permission to delete this item! ")
            continue
        break

    confirm = input("Are you sure you wish to delete this item?(y/n) \n")
    if confirm == 'y':
        print("Item deleted!")
        mycursor.execute("delete from item where item_id = (%s)", (itemID,))
        return
    else:
        print("Item NOT deleted!")
        return

def updateInventory(id: int):

    while True:
        inventory = input("What is the name of the inventory you would like to modify? ")
        if inventory == '0':
            return

        mycursor.execute("SELECT inventory_id FROM inventory WHERE Name = (%s)", (inventory,))
        try: invenID = mycursor.fetchone()[0]
        except: 
            print("No such inventory exists! ")
            continue

        mycursor.execute("SELECT catalog_id FROM inventory WHERE inventory_id = (%s) and name = (%s)", (invenID, inventory))
        catalogID = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM user_edit_inventory WHERE (user_id, inventory_id) = (%s, %s)", (id,invenID))
        try: mycursor.fetchone()[0]
        except:
            print("You do not have access to this inventory! ")
            continue
        break

    while True:
        item = input("What is the name of the item you would like to add/remove? ")
        if item == '0':
            return
        
        mycursor.execute("SELECT item_id FROM item WHERE Catalog_ID = (%s) AND Name = (%s)", (catalogID, item))
        try: itemID = mycursor.fetchone()[0]
        except: 
            print("No such item exists! ")
            continue

        mycursor.execute("SELECT quantity FROM contains_item WHERE (item_id, Inventory_ID) = (%s,%s)", (itemID, invenID))
        try: quantity = mycursor.fetchone()[0]
        except: 
            quantity = 0
        break

    while True:
        choice = input("Would you like to add or remove some of the item from your inventory? You currently have {quantity} of this item.(Add = 1, Remove = 2, Quit = 0)".format(quantity=quantity))
        try: choice = int(choice)
        except:
            print("Please enter a valid input!")
            continue
        if choice < 0 or choice > 2:
            print("Please enter a valid input! ")
            continue
        if choice == 0:
            return
        if choice == 1:
            add = int(input("How much of the item would you like to add?"))
            if add <= af.checkQuantity(itemID):
                mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (add+quantity,itemID,invenID))
                if quantity == 0:
                    mycursor.execute("INSERT INTO Contains_Item (inventory_ID, Catalog_id, item_id, quantity) VALUES (%s, %s, %s, %s)", (invenID, catalogID, itemID, add))
                db.commit()
                print("Item Added Successfully")
                break
            else:
                print ("There is not enough of this item to add to your inventory, please enter a valid number.")

        if choice == 2:
            remove = int(input("How much of the item would you like to remove?"))
            if remove <= quantity:
                mycursor.execute("UPDATE CONTAINS_ITEM SET Quantity = (%s) WHERE (Item_ID, Inventory_ID) = (%s,%s)", (quantity-remove,itemID,invenID))
                db.commit()
                print("Item Removed Successfully")
                break
            else:
                print("You are trying to remove too much of the item from your inventory, please try again.")

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

def viewItemsInCatalog():
    while True:
        catalog = input("Which catalog would you like to view items from? ")

        mycursor.execute("SELECT catalog_id FROM item_catalog WHERE Name = (%s)", (catalog,))
        try:
            catalogID = mycursor.fetchone()[0]
            break
        except:
            print("No such catalog exists! ")
            continue

    mycursor.execute("SELECT * FROM ITEM where catalog_id = (%s)", (catalogID,))
    print(f"Items in Catalog {catalog}:")
    for x in mycursor:
        print(x)

def viewItemsInInventory():
    while True:
        inventory = input("Which inventory would you like to view items from? ")

        mycursor.execute("SELECT inventory_id FROM inventory WHERE Name = (%s)", (inventory,))
        try:
            inventoryID = mycursor.fetchone()[0]
            break
        except:
            print("No such inventory exists! ")
            continue

    mycursor.execute("SELECT * FROM contains_item join item on item.item_id = contains_item.item_id WHERE contains_item.inventory_id = (%s)", (inventoryID,))
    print(f"Items in Inventory {inventory}:")
    for x in mycursor:
        print(x)

def craftItem(id: int):
    pass
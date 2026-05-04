import functionalRequirements as fr
import aggregationFunctions as af
import sampleInput as si
import mysql.connector
import re
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = db.cursor()

def createNoCommentSetup():
    with open("setup.sql","r",encoding="utf-8") as f:
        sql = f.read()

    cleaned = re.sub(r"--.*?$","",sql,flags=re.MULTILINE)

    with open("setupNoComments.sql","w",encoding="utf-8") as f:
        f.write(cleaned)

def Initial_setup():
    demo = ''

    createNoCommentSetup()
    print("Initializing setup...")
    cursor.execute("""
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = "gameCatalogs"
    """)
    result = cursor.fetchone()
    if result:
        print("Database gameCatalogs already exists!")
    else:
        print("Lets create Database gameCatalogs")

        while demo != 'y' and demo != 'n':
            demo = input("Would you like to preload with the demo data? (y/n)")

        # Create and use
        cursor.execute("CREATE DATABASE gameCatalogs")
        cursor.execute("USE gameCatalogs")

        # Read and execute setup.sql file
        with open("setupNoComments.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        statements = [s.strip() for s in sql_script.split(";") if s.strip()]

        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print("Error in statement:", stmt)
                print(e)
                break

        db.commit()

    # Finish setting up additional files
    fr.finishSetup()
    af.finishSetup()
    si.finishSetup()

    if demo == 'y':
        si.Populate_All()

    print("Setup complete.\n")


    if os.path.exists("setupNoComments.sql"):
        os.remove("setupNoComments.sql")

def menu(id = -1):
    if id == -1:
        id = fr.login() # Add the ability to sign up (new user)

    action =1
    while action != 0:
        print("----------------Welcome to the Game Catalog Database----------------")
        print("Choose your actions:")
        print("1. Create tuple\t\t\t2. Modify tuple")
        #1 will include creating catalog, inventory, and item
        #2 will include modifying existing tuples
        print("3. Delete tuple\t\t\t4. Search tuple")
        #3 will include deleting items, catalogs, and inventories or this account
        #4 will include searching catalogs and inventories and items
        print("5. Sort tuples\t\t\t6.View tuples")
        #5 will include sorting catalogs and inventories
        #6 will include viewing all tuples in the a catalog, inventory, or such
        print("7. Edit inventory\t\t8. Add access")
        #7 will include equipping items, add or remove items from inventory, craft an item
        #8 will include adding access to inventories or catalogs
        print("0. Logout")

        action = input("")
        try: action = int(action)
        except: menu(id)

        while action < 0 or action > 8:
            print("Invalid action, please choose from the menu.")
            confirm = input("press enter")
            action = menu(id)
        match action:
            # Create tuple
            case 1:
                choice = -1
                while choice < 0 or choice > 3:
                    print("What would you like to create?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Back")
                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1
                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.createCatalog(id)
                    case 2:
                        fr.createInventory(id)
                    case 3:
                        fr.createItem(id)
                    case 0:
                        menu(id)
                        break
            # Modify tuple
            case 2:
                choice = -1
                while choice < 0 or choice > 3:
                    print("What would you like to modify?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.updateCatalog(id)
                    case 2:
                        fr.updateInventory(id)
                    case 3:
                        fr.modifyItem(id)
                    case 0:
                        menu(id)
                        break
            # Delete tuple
            case 3:
                choice = -1
                while choice < 0 or choice > 3:
                    print("What would you like to delete?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Back")
                    
                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.deleteCatalog(id)
                    case 2:
                        fr.deleteInventory(id)
                    case 3:
                        fr.deleteItem(id)
                    case 0:
                        menu(id)
                        break
            # Search Tuple
            case 4:
                choice = -1
                while choice < 0 or choice > 3:
                    print("What would you like to search for?")
                    print("1. Item in a Catalog")
                    print("2. Item in an Inventory")
                    print("3. Name of a Catalog or Inventory")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.searchCatalog(id)
                    case 2:
                        fr.searchInventory(id)
                    case 3:
                        fr.searchSystem(id)
                    case 0:
                        menu(id)
                        break
            # Sort tuples
            case 5:
                choice = -1
                while choice < 0 or choice > 2:
                    print("What would you like to sort?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 2:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.sortCatalog(id)
                    case 2:
                        fr.sortInventory(id)
                    case 0:
                        menu(id)
                        break
            # View tuples
            case 6:
                choice = -1
                while choice < 0 or choice > 3:
                    print("What would you like to view?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.viewCatalog()
                    case 2:
                        fr.viewInventory()
                    case 3:
                        fr.viewItem()
                    case 4:
                        af.findCountCatalogs(id)
                    case 5:
                        af.findCountInventories(id)
                    case 6:
                        found = 0
                        catalogID = 0
                        while found == 0:
                            print("Here are your options:")
                            cursor.execute("SELECT Name FROM ITEM_CATALOG")
                            for x in cursor:
                                for y in x:
                                    print(y)
                            catalog = input("Which item catalog would you like to know the amount of items.")
                            if catalog == '0':
                                return
                            
                            cursor.execute("SELECT Catalog_ID FROM ITEM_CATALOG WHERE Name = (%s)", (catalog,))
                            
                            for x in cursor:
                                found += 1
                                catalogID = x[0]

                            if found == 0:
                                print("That item catalog does not exist. Please enter a valid catalog.")
                        af.findCountItemsCatalog(catalogID)
                    case 7:
                        found = 0
                        invenID = 0
                        while found == 0:
                            print("Here are your options:")
                            cursor.execute("SELECT Name FROM INVENTORY")
                            for x in cursor:
                                for y in x:
                                    print(y)
                            inven = input("Which inventory would you like to know the amount of items.")
                            if catalog == '0':
                                break
                            
                            cursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
                            
                            for x in cursor:
                                found += 1
                                invenID = x[0]

                            if found == 0:
                                print("That inventory does not exist. Please enter a valid inventory.")
                        af.findCountItemsInventory(invenID)
                    case 8:
                        found = 0
                        invenID = 0
                        while found == 0:
                            print("Here are your options:")
                            cursor.execute("SELECT Name FROM INVENTORY")
                            for x in cursor:
                                for y in x:
                                    print(y)
                            inven = input("Which inventory would you like to know the amount of items.")
                            if catalog == '0':
                                break
                            
                            cursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
                            
                            for x in cursor:
                                found += 1
                                invenID = x[0]

                            if found == 0:
                                print("That inventory does not exist. Please enter a valid inventory.")
                        af.findMaxWeight(invenID)
                    case 9:
                        found = 0
                        invenID = 0
                        while found == 0:
                            print("Here are your options:")
                            cursor.execute("SELECT Name FROM INVENTORY")
                            for x in cursor:
                                for y in x:
                                    print(y)
                            inven = input("Which inventory would you like to know the amount of items.")
                            if catalog == '0':
                                break
                            
                            cursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
                            
                            for x in cursor:
                                found += 1
                                invenID = x[0]

                            if found == 0:
                                print("That inventory does not exist. Please enter a valid inventory.")
                        af.findMinWeight(invenID)
                    case 10:
                        found = 0
                        invenID = 0
                        while found == 0:
                            print("Here are your options:")
                            cursor.execute("SELECT Name FROM INVENTORY")
                            for x in cursor:
                                for y in x:
                                    print(y)
                            inven = input("Which inventory would you like to know the amount of items.")
                            if catalog == '0':
                                break
                            
                            cursor.execute("SELECT Inventory_ID FROM INVENTORY WHERE Name = (%s)", (inven,))
                            
                            for x in cursor:
                                found += 1
                                invenID = x[0]

                            if found == 0:
                                print("That inventory does not exist. Please enter a valid inventory.")
                        af.findSumWeight(invenID)
                    case 0:
                        menu(id)
                        break
            # Edit inventory
            case 7:
                choice = -1
                while choice < 0 or choice > 3:
                    print("How would you like to edit your inventory?")
                    print("1. Equip an Item")
                    print("2. Add or Remove an Item")
                    print("3. Craft an Item")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.equipItem(id)
                    case 2:
                        fr.updateInventory(id)
                    case 3:
                        fr.craftItem(id)
                    case 0:
                        menu(id)
                        break
            # Add access
            case 8:
                choice = -1
                while choice < 0 or choice > 2:
                    print("Would you like to add access to a catalog or an inventory?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 2:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.giveCatalogAccess(id)
                    case 2:
                        fr.giveInventoryAccess(id)
                    case 0:
                        menu(id)
                        break
                    
                
            # Logout  
            case 0:
                print("You have been logged out")
                db.commit()
                menu()

        print()
        input("Press enter to continue")
        menu(id)


def main():
    Initial_setup()
    menu()

if __name__ == "__main__":
    main()
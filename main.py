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
        print("5. Sort tuples\t\t\t6. View tuples")
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
                while choice < 0 or choice > 4:
                    print("What would you like to modify?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("4. User Profile")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 4:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.updateCatalog(id)
                    case 2:
                        fr.modifyInventory(id)
                    case 3:
                        fr.modifyItem(id)
                    case 4:
                        fr.updateUser(id)
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
                while choice < 0 or choice > 16:
                    print("What would you like to view?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("4. Number of your Catalogs")
                    print("5. Number of your Inventories")
                    print("6. Number of items in a chosen Catalog")
                    print("7. Number of items in a chosen Inventory")
                    print("8. Max Item Weight in a chosen Inventory")
                    print("9. Min Item Weight in a chosen Inventory")
                    print("10. Total Item Weight in a chosen Inventory")
                    print("11. Creators who can edit a chosen Catalog")
                    print("12. Users who can edit a chosen Inventory")
                    print("13. Max Item Weight in a chosen Catalog")
                    print("14. Min Item Weight in a chosen Catalog")
                    print("15. Items in Catalog")
                    print("16. Items in Inventory")
                    print("0. Back")

                    choice = input("")
                    try: choice = int(choice)
                    except: choice = -1

                    if choice < 0 or choice > 16:
                        print("Invalid choice, please try again")
                match choice:
                    case 1:
                        fr.viewCatalog()
                    case 2:
                        fr.viewInventory()
                    case 3:
                        fr.viewItem()
                    case 4:
                        print(af.findCountCatalogs(id))
                    case 5:
                        print(af.findCountInventories(id))
                    case 6:
                        print(af.findCountItemsCatalog())
                    case 7:
                        print(af.findCountItemsInventory())
                    case 8:
                        print(af.findMaxWeight())
                    case 9:
                        print(af.findMinWeight())
                    case 10:
                        print(af.findSumWeight())
                    case 11:
                        print(af.findCountCreatorsEditCatalog())
                    case 12:
                        print(af.findCountUsersEditInventory())
                    case 13:
                        print(af.getMaxWeightCatalog())
                    case 14: 
                        print(af.getMinWeightInventory())
                    case 15:
                        print("ok")
                        fr.viewItemsInCatalog()
                    case 16:
                        fr.viewItemsInInventory()
                    case 0:
                        menu(id)
                        break
            # Edit inventory
            case 7:
                choice = -1
                while choice < 0 or choice > 2:
                    print("How would you like to edit your inventory?")
                    print("1. Equip an Item")
                    print("2. Add or Remove an Item")
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
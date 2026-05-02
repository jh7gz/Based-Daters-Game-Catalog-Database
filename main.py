import functionalRequirements as fr
#import aggregationFunctions as af
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()

def Initial_setup():
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

        # Create and use
        cursor.execute("CREATE DATABASE gameCatalogs")
        cursor.execute("USE gameCatalogs")

        # Read and execute setup.sql file
        with open("setupNoComments.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()
        cursor.execute(sql_script)
    print("Setup complete.\n")

def menu():
    id = fr.login()
    action =1
    while action != 0:
        print("----------------Welcome to the Game Catalog Database----------------")
        print("Choose your actions:")
        print("1. Create tuple\t\t\t2. Add access")
        #1 will include creating catalog, inventory, and item
        #2 will include adding access to inventories or catalogs
        print("3. Search tuples\t\t\t4. Delete tuples")
        #3 will include searching catalogs and inventories
        #4 will include deleting items, catalogs, and inventories
        print("5. Update inventory\t\t\t6.Creator Actions")
        #5 will include equipping items, add or remove items from inventory, craft an item
        #6 will include changing quantity of items and modifying items
        print("7. Sort tuples\t\t\t0. Quit")
        #7 will include sorting catalogs and inventories
        action = int(input(""))
        while action < 0 or action > 7:
            print("Invalid action, please choose from the menu.")
            confirm = input("press enter")
            action = menu()
        match action:
            case 1:
                choice = 1
                while choice > 0 or choice < 4:
                    print("What would you like to create?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.createCatalog(id)
                            menu()
                        case 2:
                            fr.createInventory(id)
                            menu()
                        case 3:
                            fr.createItem(id)
                            menu()
                        case 0:
                            quit()
            case 2:
                choice = 1
                while choice > 0 or choice < 3:
                    print("Would you like to add access to a catalog or an inventory?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 2:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.giveCatalogAccess(id)
                            menu()
                        case 2:
                            fr.giveInventoryAccess(id)
                            menu()
                        case 0:
                            quit()
            case 3:
                choice = 1
                while choice > 0 or choice < 4:
                    print("What would you like to search for?")
                    print("1. Item in a Catalog")
                    print("2. Item in an Inventory")
                    print("3. Name of a Catalog or Inventory")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.searchCatalog(id)
                            menu()
                        case 2:
                            fr.searchInventory(id)
                            menu()
                        case 3:
                            fr.searchSystem(id)
                            menu()
                        case 0:
                            quit()
            case 4:
                choice = 1
                while choice > 0 or choice < 4:
                    print("What would you like to delete?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("3. Item")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.deleteCatalog(id)
                            menu()
                        case 2:
                            fr.deleteInventory(id)
                            menu()
                        case 3:
                            fr.deleteItem(id)
                            menu()
                        case 0:
                            quit()
            case 5:
                choice = 1
                while choice > 0 or choice < 4:
                    print("How would you like to update your inventory?")
                    print("1. Equip an Item")
                    print("2. Add or Remove an Item")
                    print("3. Craft an Item")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 3:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.equipItem(id)
                            menu()
                        case 2:
                            fr.updateInventory(id)
                            menu()
                        case 3:
                            fr.craftItem(id)
                            menu()
                        case 0:
                            quit()
            case 6:
                choice = 1
                while choice > 0 or choice < 3:
                    print("What creator action would you like to take?")
                    print("1. Check/Update Quantity")
                    print("2. Modify Item")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 2:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.checkQuantity(id)
                            menu()
                        case 2:
                            fr.modifyItem(id)
                            menu()
                        case 0:
                            quit()
            case 7:
                choice = 1
                while choice > 0 or choice < 3:
                    print("What would you like to sort?")
                    print("1. Catalog")
                    print("2. Inventory")
                    print("0. Quit")
                    choice = int (input(""))
                    if choice < 0 or choice > 2:
                        print("Invalid choice, please try again")
                        choice = int(input(""))
                    match choice:
                        case 1:
                            fr.sortCatalog(id)
                            menu()
                        case 2:
                            fr.sortInventory(id)
                            menu()
                        case 0:
                            quit()
            case 0:
                quit()
                        

    pass

def main():
    Initial_setup()
    menu()

if __name__ == "__main__":
    main()
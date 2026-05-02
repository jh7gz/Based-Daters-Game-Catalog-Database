import mysql.connector

db = None
mycursor = None

def setup_database_if_needed():
    print("Initializing database if needed...")

    db = mysql.connector.connect(
        host="localhost",
        user="SA",
        password="Database2026",
    )

    mycursor = db.cursor()

    # 1. Create DB FIRST
    mycursor.execute("SHOW DATABASES LIKE 'gameCatalogs'")
    exists = mycursor.fetchone()
    if not exists:
        print("Creating database...")
        mycursor.execute("CREATE DATABASE gameCatalogs")

    # 2. Switch into DB immediately
    mycursor.execute("USE gameCatalogs")

    # 3. NOW run schema
    mycursor.execute("SHOW TABLES LIKE 'USERS'")
    exists = mycursor.fetchone()

    if not exists:
        print("Schema not found. Creating tables...")
        with open("setup.sql", "r") as setup:
            sql_script = setup.read()
            statements = sql_script.split(";")

            for statement in statements:
                statement = statement.strip()
                if statement:
                    mycursor.execute(statement)

        db.commit()

    else:
        print("Schema already exists. Skipping setup.")

    print("Database initialized.")

def login():
    found = 0
    while found == 0:
        id = input("Please enter your Profile Name (enter 0 to quit or 1 to create a new account): ")
        if id == '0':
            quit()

        while id == '1':
            id = input("Please enter your new Profile Name : ")
            mycursor.execute("SELECT * FROM User WHERE Profile_Name = (%s)", (id,))
            for x in mycursor:
                found += 1
            if found == 0:
                psswrd = input("That Profile Name is available. Please enter a password.")
                first = input("Please enter your first name")
                last = input("Please enter your last name")
                middle = input("Please enter your middle initial")
                try:
                    mycursor.execute("INSERT INTO User(Profile_Name,Password,F_name,M_Init,L_Name) VALUES (%s,%s,%s,%s,%s)", (id,psswrd,first,middle,last))
                    db.commit()
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
                print("New account created, proceeding to login")
            if found != 0:
                print("That Profile Name is in use, please try again")
                id = '1'


        mycursor.execute("SELECT * FROM User WHERE Profile_Name = (%s)", (id,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That Profile Name does not exist. Please enter a valid profile name.")
    
    correct = 0
    while correct == 0:
        pswd = input("Please enter your password (enter 0 to quit): ")
        if pswd == '0':
            quit()
        mycursor.execute("SELECT * FROM User WHERE Profile_Name = (%s) AND Password = (%s)", (id, pswd))
        for x in mycursor:
            correct += 1
        if correct == 0:
            print("That password is not correct. Please enter the correct password.")

def createCatalog():
    found = 0
    while found == 0:
        name = input("What would you like the name of the Item Catalog to be?")
        mycursor.execute("SELECT * FROM Catalog WHERE Name = (%s)", (name,))
        for x in mycursor:
            found += 1
        if found != 0:
            print("That item catlog already exists. Please enter a valid new catalog name.")
    
    try:
        mycursor.execute("INSERT INTO ITEM_CATALOG(Name) VALUES (%s)", (name,))
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New catalog created successfully.")

def createInventory():
    found = 0
    while found == 0:
        catalog = input("Which item catalog would you like to create an inventory for.")
        mycursor.execute("SELECT * FROM Catalog WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
    
    name = input("What would you like the name of your inventory to be?")
    try:
        mycursor.exectute("INSERT INTO INVENTORY(Name) VALUES (%s)", (name,))
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New inventory created successfully.")

def createItem():
    found = 0
    while found == 0:
        catalog = input("Which item catalog would you like to create an item for.")
        mycursor.execute("SELECT * FROM Catalog WHERE Name = (%s)", (catalog,))
        for x in mycursor:
            found += 1
        if found == 0:
            print("That item catlog does not exist. Please enter a valid catalog.")
    
    found = 0
    while found == 0:
        name = input("What would you like the name of your item to be?")
        mycursor.execute("SELECT * FROM Catalog WHERE Name = (%s)", (name))
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
        mycursor.exectute("INSERT INTO Item(Weight, Overall_Quan,Description,Category,Rarity,Name,C_Flag,R_Flag,W_A_Flag,UI_Flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (weight,number,desc,cat,rarity,name,consumable,resource,weaparm,upgrade))
        db.commit()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    print("New item created successfully.")


 

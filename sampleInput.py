import random
import aggregationFunctions as af
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

cursor = db.cursor()

def finishSetup():
    cursor.execute("USE gameCatalogs")

def Populate_WEAPON_ARMOR_EQUIPPED(numInventories: int):
    for i in range(numInventories):
        inventoryID = i + 1
        catalogID = cursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Inventory_ID = %s", (inventoryID,))
        numEquipped = random.randint(0, 4)
        numOptions = cursor.execute("SELECT COUNT(*) FROM CONTAINS_ITEMS WHERE Inventory_ID = %s AND WA_Flag = 1", (inventoryID,))
        for j in range(numEquipped):
            cursor.execute("SELECT Item_ID FROM CONTAINS_ITEMS WHERE Inventory_ID = %s AND WA_Flag = 1", (inventoryID,))
            if numOptions > j:
                itemID = cursor.fetchone()[j]
            cursor.execute("INSERT INTO WEAPON_ARMOR_EQUIPPED(Item_ID, Inventory_ID, Catalog_ID) VALUES (%s, %s, %s)", (itemID, inventoryID, catalogID))
    
    print("Succesfully populated WEAPON_ARMOR_EQUIPPED")
    #cursor.execute("SELECT * FROM WEAPON_ARMOR_EQUIPPED")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_CONTAINS_ITEMS(numInventories: int, maxNumItemsPerInventory: int):
    for i in range(numInventories):
        numItemsInInventory = random.choice(range(1, maxNumItemsPerInventory + 1))
        inventoryID = i+1
        catalogID = cursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Inventory_ID = %s", (inventoryID,))
        for j in range(numItemsInInventory):
            minID = cursor.execute("SELECT MIN(Item_ID) FROM ITEMS WHERE Catalog_ID = %s", (catalogID,))
            maxID = cursor.execute("SELECT MAX(Item_ID) FROM ITEMS WHERE Catalog_ID = %s", (catalogID,))
            itemID = random.choice([minID, maxID])
            quantityLeft = af.checkQuantity(itemID)
            quantity = random.choice(range(1, quantityLeft + 1))
            cursor.execute("INSERT INTO CONTAINS_ITEMS(Inventory_ID, Catalog_ID, Item_ID, Quantity) VALUES (%s, %s, %s, %s)", (inventoryID, catalogID, itemID, quantity))
    print("Succesfully populated CONTAINS_ITEMS")
    #cursor.execute("SELECT * FROM CONTAINS_ITEMS")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_CREATOR_EDIT_CATALOG(numUsers: int, numCatalogs: int):
    for i in range(numCatalogs):
        numEditors = random.choice(range(1, numUsers/2))
        for j in range(numEditors):
            user_ID = random.choice(range(1, numUsers + 1))
            catalogID = i + 1
            cursor.execute("INSERT INTO CREATOR_EDIT_CATALOG(User_ID, Catalog_ID) VALUES (%s, %s)", (user_ID, catalogID))
            cursor.execute("UPDATE USERS SET Creator_Flag = 1 WHERE User_ID = %s", (user_ID,))
    print("Succesfully populated CREATOR_EDIT_CATALOG")
    #cursor.execute("SELECT * FROM CREATOR_EDIT_CATALOG")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_USER_EDIT_INVENTORY(numUsers: int, numInventories: int):
    for i in range(numInventories):
        numEditors = random.choice(range(1, numUsers/2))
        inventoryID = i + 1
        catalogID = cursor.execute("SELECT Catalog_ID FROM INVENTORY WHERE Inventory_ID = %s", (inventoryID,))
        for j in range(numEditors):
            user_ID = random.choice(range(1, numUsers + 1))
            cursor.execute("INSERT INTO USER_EDIT_INVENTORY(User_ID, Inventory_ID, Catalog_ID) VALUES (%s, %s, %s)", (user_ID, inventoryID, catalogID))
            cursor.execute("UPDATE USERS SET Player_Flag = 1 WHERE User_ID = %s", (user_ID,))
    print("Succesfully populated USER_EDIT_INVENTORY")
    #cursor.execute("SELECT * FROM USER_EDIT_INVENTORY")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_USER_EMAIL(numUsers: int, numEmails: int):
    for i in range(numEmails):
        randUserID = random.choice(range(1, numUsers + 1))
        profileName = cursor.execute("SELECT Profile_Name FROM USERS WHERE User_ID = %s", (randUserID,))
        email = f"{profileName}@email.com"
        cursor.execute("INSERT INTO USER_EMAIL(User_ID, Email) VALUES (%s, %s)", (randUserID, email))
    print("Succesfully populated USER_EMAIL")
    #cursor.execute("SELECT * FROM USER_EMAIL")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_USERS(numUsers: int, numEmails: int):
    profileNameList = ('JamesWeiss01', 'GabeWeeks43', 'JamalMoody87', 'RudolfHolland34', 'ChuckBuck76', 'EvanPicks79', 'BenjaminBradford89', 'NathanSimpsons23', 'SeanSanchez68')
    fNameList = ('James', 'Gabe', 'Jamal', 'Rudolf', 'Chuck', 'Evan', 'Benjamin', 'Nathan', 'Sean')
    mInitList = ('A', 'B', '', '', 'E', 'F', '', 'H', 'I')
    lNameList = ('Weiss', 'Weeks', 'Moody', 'Holland', 'Buck', 'Picks', 'Bradford', 'Simpsons', 'Sanchez')

    for i in range(numUsers):
        fName = random.choice(fNameList)
        mInit = random.choice(mInitList)
        lName = random.choice(lNameList)
        profileName = profileNameList[i]
        password = "pass"
        pFlag = 0
        cFlag = 0
        cursor.execute("INSERT INTO USERS(Profile_Name, Password, F_Name, M_Init, L_Name, Player_Flag, Creator_Flag) VALUES (%s, %s, %s, %s, %s, %s, %s)", (profileName, password, fName, mInit, lName, pFlag, cFlag))
    print("Succesfully populated USERS")
    #cursor.execute("SELECT * FROM USERS")
    #for x in cursor:
        #print(x)
    db.commit()
    Populate_USER_EMAIL(numUsers, numEmails)

def Populate_ITEM_CATALOG(numCatalogs: int):
    for i in range(numCatalogs):
        name = f"Catalog_{i}"
        cursor.execute("INSERT INTO CATALOGS(Name) VALUES (%s)", (name,))
    print("Succesfully populated CATALOGS")
    #cursor.execute("SELECT * FROM CATALOGS")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_INVENTORY(numCatalogs: int):
    
    for i in range(numCatalogs):
        numInventories = random.randint(1, 5)
        for j in range(numInventories):
            name = f"Inventory_C{i+1}_I{j+1}"
            catalog_ID = i + 1
            cursor.execute("INSERT INTO INVENTORIES(Catalog_ID, Name) VALUES (%s, %s)", (catalog_ID, name))
    print("Succesfully populated INVENTORIES")
    #cursor.execute("SELECT * FROM INVENTORIES")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_ITEM(numItems: int, numCatalogs: int):

    for i in range(numItems):
        item_ID = i+1
        name = f"Item_{item_ID}"
        catalog_ID = random.choice(range(1, numCatalogs + 1))
        weight = round(random.uniform(0.1, 10.0), 2)
        overall_quan = random.randint(1, 100)
        description = f"TClever description for Item {item_ID}."
        category = random.choice(['Potion', 'Weapon', 'Armor', 'Unknown', ''])
        rarity = random.choice(['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'])
        c_flag = random.choice([0, 1])
        r_flag = random.choice([0, 1])
        wa_flag = random.choice([0, (c_flag + 1)%2])
        ui_flag = wa_flag and r_flag

        # Have an item effect
        if (c_flag or wa_flag) and random.choice([0, 1, 2, 3]) == 0:
            numEffects = random.randint(1, 3)
            for j in range(numEffects):
                effect = random.choice(['Heal', 'Damage', 'Buff', 'Debuff'])
                constIncrease = random.randint(-5, 10)
                percentIncrease = random.randint(-200, 200)
                duration = random.randint(1, 60)
                cursor.execute("INSERT INTO ITEM_EFFECTS(Item_ID, Catalog_ID, Effect, Const_Inc, Percent_Inc, Duration) VALUES (%s, %s, %s, %s, %s, %s)", (item_ID, catalog_ID, effect, constIncrease, percentIncrease, duration))

        # Insert into ITEM
        cursor.execute("INSERT INTO ITEMS(Catalog_ID, Weight, Overall_Quan, Description, Category, Rarity, C_Flag, R_Flag, Wa_Flag, Ui_Flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (catalog_ID, weight, overall_quan, description, category, rarity, c_flag, r_flag, wa_flag, ui_flag))
        
        # Have a range and type
        numRanges = random.randint(1, 3)
        numTypes = random.randint(1, 3)
        if (wa_flag):
            # Add ranges to ITEM_WEAPON_ARMOR_RANGE
            for j in range(numRanges):
                range = random.randint(1, 30)
                damage = random.randint(1, 20)
                cursor.execute("INSERT INTO ITEM_WEAPON_ARMOR_RANGE(Item_ID, Catalog_ID, WARange, Damage) VALUES (%s, %s, %s, %s)", (item_ID, catalog_ID, range, damage))
            # Add types to ITEM_WEAPON_ARMOR_TYPE
            for j in range(numTypes):
                type = random.choice(['Melee', 'Ranged', 'Magic', 'Heavy Rock'])
                cursor.execute("INSERT INTO ITEM_WEAPON_ARMOR_TYPE(Item_ID, Catalog_ID, WAType) VALUES (%s, %s, %s)", (item_ID, catalog_ID, type))

    print("Succesfully populated ITEMS, ITEM_EFFECTS, ITEM_WEAPON_ARMOR_RANGE, and ITEM_WEAPON_ARMOR_TYPE")
    #cursor.execute("SELECT Item_ID FROM ITEMS")
    #for x in cursor:
        #printItemInfo(Item_ID)
    db.commit()

def Populate_All():
    # Main tables
    numUsers = 10
    numEmails = 20
    numCatalogs = 4
    numItems = 50
    Populate_USERS(numUsers, numEmails)
    Populate_ITEM_CATALOG(numCatalogs)
    Populate_INVENTORY(numCatalogs)
    numInventories = cursor.execute("SELECT COUNT(*) FROM INVENTORY")
    Populate_ITEM(numItems, numCatalogs)

    # Relation tables
    maxNumItemsPerInventory = 20
    Populate_USER_EDIT_INVENTORY(numUsers, numInventories)
    Populate_CREATOR_EDIT_CATALOG(numUsers, numCatalogs)
    Populate_CONTAINS_ITEMS(numInventories, maxNumItemsPerInventory)
    Populate_WEAPON_ARMOR_EQUIPPED(numInventories)



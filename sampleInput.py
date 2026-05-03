import random
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

cursor = db.cursor()

def finishSetup():
    cursor.execute("USE gameCatalogs")

def Populate_USERS():
    profileNameList = ('JamesWeiss01', 'GabeWeeks43', 'JamalMoody87', 'RudolfHolland34', 'ChuckBuck76', 'EvanPicks79', 'BenjaminBradford89', 'NathanSimpsons23', 'SeanSanchez68')
    fNameList = ('James', 'Gabe', 'Jamal', 'Rudolf', 'Chuck', 'Evan', 'Benjamin', 'Nathan', 'Sean')
    mInitList = ('A', 'B', '', '', 'E', 'F', '', 'H', 'I')
    lNameList = ('Weiss', 'Weeks', 'Moody', 'Holland', 'Buck', 'Picks', 'Bradford', 'Simpsons', 'Sanchez')

    for i in range(10):
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

def Populate_CATALOGS():
    
    for i in range(10):
        name = f"Catalog_{i}"
        cursor.execute("INSERT INTO CATALOGS(Name) VALUES (%s)", (name,))
    print("Succesfully populated CATALOGS")
    #cursor.execute("SELECT * FROM CATALOGS")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_INVENTORIES():
    
    for i in range(10):
        name = f"Inventory_{i}"
        catalog_ID = i + 1
        cursor.execute("INSERT INTO INVENTORIES(Catalog_ID, Name) VALUES (%s, %s)", (catalog_ID, name))
    print("Succesfully populated INVENTORIES")
    #cursor.execute("SELECT * FROM INVENTORIES")
    #for x in cursor:
        #print(x)
    db.commit()

def Populate_ITEMS():

    for i in range(10):
        name = f"Item_{i}"
        catalog_ID = i + 1
        weight = round(random.uniform(0.1, 10.0), 2)
        overall_quan = random.randint(1, 100)
        description = f"TClever name {i}."
        category = random.choice(['Potion', 'Weapon', 'Armor', 'Unknown', ''])
        rarity = random.choice(['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'])
        c_flag = random.choice([0, 1])
        r_flag = random.choice([0, 1])
        wa_flag = random.choice([0, 1])
        ui_flag = random.choice([0, 1])
        cursor.execute("INSERT INTO ITEMS(Catalog_ID, Name) VALUES (%s, %s)", (catalog_ID, name))
    print("Succesfully populated ITEMS")
    #cursor.execute("SELECT * FROM ITEMS")
    #for x in cursor:
        #print(x)
    db.commit()


"""
Item_ID int AI PK 
Catalog_ID int PK 
Weight decimal(5,2) 
Overall_Quan int 
Description text 
Category varchar(50) 
Rarity varchar(50) 
Name varchar(100) 
C_Flag bit(1) 
R_Flag bit(1) 
WA_Flag bit(1) 
UI_Flag bit(1)
"""


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


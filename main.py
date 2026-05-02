#import functionalRequirements as fr
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
    pass

def main():
    Initial_setup()
    menu()

if __name__ == "__main__":
    main()
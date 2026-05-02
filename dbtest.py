import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()

# try 1: no database connected
def try1():
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print("Connected to:", result)

# try 3: check if the database exists
def try3():
    db_name = "test"
    cursor.execute("""
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = %s
    """, (db_name,))
    result = cursor.fetchone()
    if result:
        print("Database", db_name, "exists!")
    else:
        print("Database", db_name, "does NOT exist.")

# try 4: check if the database exists and create it if it doesn't
def try4():
    db_name = "lemon"
    cursor.execute("""
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = %s
    """, (db_name,))
    result = cursor.fetchone()
    if result:
        print("Database", db_name, "exists!")
    else:
        print("Lets create Database", db_name)

def try5():
    db_name = "gameCatalog"
    cursor.execute("""
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = %s
    """, (db_name,))
    result = cursor.fetchone()
    if result:
        print("Database", db_name, "exists!")
    else:
        print("Lets create Database", db_name)

        # Read SQL file
        with open("setup.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Execute multiple statements
        for statement in sql_script.split(";"):
            print("One down")
            stmt = statement.strip()
            if stmt:  # ignore empty lines/comments-only chunks
                cursor.execute(stmt)

        # Do I need this: conn.commit()

# Try 6: Same as try5, but does setup.sql as a whole
def try6():
    db_name = "gameCatalogs"
    cursor.execute("""
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = %s
    """, (db_name,))
    result = cursor.fetchone()
    if result:
        print("Database", db_name, "exists!")
    else:
        print("Lets create Database", db_name)

        # Create and use
        cursor.execute(f"CREATE DATABASE {db_name}")
        cursor.execute(f"USE {db_name}")

        # Read SQL file
        with open("setupNoComments.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Execute multiple statements
        cursor.execute(sql_script)


try6()

conn.commit() 
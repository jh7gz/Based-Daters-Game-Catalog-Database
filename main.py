import functionalRequirements as fr
import aggregationFunctions as af

def menu():
    # TODO
    pass

def main():
    fr.setup_database_if_needed()
    af.connectDB()
    menu()
    
if __name__ == "__main__":
    main()
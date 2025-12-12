import psycopg as pg
import config
import search_data
import add_data
import remove_data 
import edit_data
import analyze_data

def main():
    # connection info
    hst = config.HOST
    usr = config.USER
    pwd = config.PASSWORD
    dat = config.DATABASE

    # make a connection
    with pg.connect(host = hst, user = usr, password = pwd, dbname = dat) as cn:
        print("\n")
        print("-------------------------------------------------")
        print("         WELCOME TO THE TV SHOW DATABASE         ")
        print("-------------------------------------------------")
        print("\n")

        while True:
            print("Menu: ")
            print("\t1. Search Data")
            print("\t2. Add Data")
            print("\t3. Remove Data")
            print("\t4. Edit Data")
            print("\t5. Analyze Data")
            print("\t6. Exit\n")

            choice = input("Enter your choice (1-6): ")
            print("\n")
            match choice:
                case "1":
                    search_curr_data(cn)
                case "2":
                    add_new_data(cn)
                case "3":
                    remove_curr_data(cn)
                case "4":
                    edit_old_data(cn)
                case "5":
                    analyze_curr_data(cn)
                case "6":
                    break

def search_curr_data(cn):
    search_data.menu(cn)

def add_new_data(cn):
    add_data.menu(cn)

def remove_curr_data(cn):
    remove_data.menu(cn)

def edit_old_data(cn):
    edit_data.menu(cn)

def analyze_curr_data(cn):
    analyze_data.menu(cn)

if __name__ == '__main__':

    main()
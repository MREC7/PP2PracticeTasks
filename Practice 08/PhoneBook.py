import psycopg2
import csv
from database import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
def init_db():
    with open("init_db.sql", "r") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
def add_contact(name, phone):
    command = "insert into contacts(name, phone) values(%s, %s)"
    with conn.cursor() as cur:
        cur.execute(command, (name, phone))
        conn.commit()
def add_contact_console():
    name = input("Please enter name: ")
    phone = input("Please enter phone number: ")
    add_contact(name, phone)
    print(f"{name} added to phone contacts.")
def add_contact_csv(file):
    command = "insert into contacts(name, phone) values(%s, %s)"
    with conn.cursor() as cur:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                name, phone = row
                cur.execute(command, (name, phone))
            conn.commit()
        print(f"Added contacts from CSV.")
def get_all_contacts():
    command = "select * from contacts order by name"
    with conn.cursor() as cur:
        cur.execute(command)
        return cur.fetchall()
def search(pattern):
    with conn.cursor() as cur:
        cur.execute("select * from search_contacts(%s)", (pattern,))
        return cur.fetchall()
def change_name(phone, name):
    command = "update contacts set name = %s where phone = %s"
    with conn.cursor() as cur:
        cur.execute(command, (name, phone))
        conn.commit()
        print(f"Successfully renamed contact.")
def change_phone(phone, name):
    command = "update contacts set phone = %s where name = %s"
    with conn.cursor() as cur:
        cur.execute(command, (phone, name))
        conn.commit()
        print(f"Successfully changed {name}'s phone number.")
def delete_by_name(name):
    command = "delete from contacts where name = %s"
    with conn.cursor() as cur:
        cur.execute(command, (name,))
        conn.commit()
        print(f"Deleted {name} from contacts.")
def delete_by_phone(phone):
    command = "delete from contacts where phone = %s"
    with conn.cursor() as cur:
        cur.execute(command, (phone,))
        conn.commit()
        print(f"Deleted {phone} from contacts.")
def insert_or_update(name, phone):
    with conn.cursor() as cur:
        cur.execute("call insert_or_update_user(%s, %s)", (name, phone))
        conn.commit()
def get_paginated(limit, offset):
    with conn.cursor() as cur:
        cur.execute("select * from get_contacts_paginated(%s, %s)", (limit, offset))
        return cur.fetchall()
def delete_contact(value):
    with conn.cursor() as cur:
        cur.execute("call delete_contact(%s)", (value,))
        conn.commit()
def print_contacts(contacts):
    if not contacts:
        print("No contacts.")
        return
    for c in contacts:
        print(f"[{c[0]}] {c[1]} --- {c[2]}")
def main():
    init_db()
    while True:
        print("\n------- Contacts -------")
        print("1) Display contacts.")
        print("2) Add contact.")
        print("3) Import contact from CSV.")
        print("4) Search.")
        print("5) Change contact name.")
        print("6) Change contact phone.")
        print("7) Delete contact by name.")
        print("8) Delete contact by phone.")
        print("9) Add or update contact.")
        print("10) Add multiple users.")
        print("11) Paginate contacts.")
        print("12) Delete contact.")
        print("0) Exit.")
        choice = input("\nChoice: ")
        match choice:
            case "0": break
            case "1": print_contacts(get_all_contacts())
            case "2": add_contact_console()
            case "3": add_contact_csv("contacts.csv")
            case "4":
                pattern = input("Search: ")
                print_contacts(search(pattern))
            case "5":
                phone = input("Phone: ")
                name = input("New name: ")
                change_name(phone, name)
            case "6":
                name = input("Name: ")
                phone = input("New phone: ")
                change_phone(phone, name)
            case "7":
                name = input("Name: ")
                delete_by_name(name)
            case "8":
                phone = input("Phone: ")
                delete_by_phone(phone)
            case "9":
                name = input("Name: ")
                phone = input("Phone: ")
                insert_or_update(name, phone)
            case "10":
                names = input("Names(comma separated): ").split(",")
                phones = input("Phones(comma separated): ").split(",")
                with conn.cursor() as cur:
                    cur.execute("call insert_many_users(%s, %s, null)", (names, phones))
                    conn.commit()
            case "11":
                limit = int(input("Limit: "))
                offset = int(input("Offset: "))
                print_contacts(get_paginated(limit, offset))
            case "12":
                value = input("Value(name or phone): ")
                delete_contact(value)
                print("Successfully deleted contact.")
            case _:
                print("Unexpected input. Try again.")
    conn.close()
    print("Exiting...")
if __name__ == "__main__":
    main()
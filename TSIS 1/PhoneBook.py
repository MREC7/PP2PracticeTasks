import psycopg2
import csv
import json
from datetime import datetime, date
from database import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def format_date(value):
    if not value:
        return "-"
    try:
        return value.strftime("%d.%m.%Y")
    except:
        return str(value)

def parse_date_safe(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except:
        return None


def init_db():
    with open("init_db.sql", "r") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def add_contact(name, phone, email=None, birthday=None):
    birthday = parse_date_safe(birthday)

    with conn.cursor() as cur:
        cur.execute("""
            insert into contacts(name, email, birthday)
            values(%s, %s, %s)
            returning id
        """, (name, email, birthday))
        cid = cur.fetchone()[0]

        cur.execute("""
            insert into phones(contact_id, phone, type)
            values(%s, %s, 'mobile')
        """, (cid, phone))

        conn.commit()


def add_contact_console():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email(optional): ")
    birthday = input("Birthday YYYY-MM-DD(optional): ")

    birthday = parse_date_safe(birthday)

    add_contact(name, phone, email or None, birthday)


def add_phone(name, phone, ptype):
    with conn.cursor() as cur:
        cur.execute("call add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()


def get_all_contacts():
    query = """
    select c.id, c.name, c.email,
           coalesce(g.name, 'No group'),
           coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    left join phones p on p.contact_id = c.id
    left join groups g on c.group_id = g.id
    group by c.id, g.name
    order by c.name
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def search(pattern):
    query = """
    select c.id, c.name, c.email,
           coalesce(g.name, 'No group'),
           coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    left join phones p on p.contact_id = c.id
    left join groups g on c.group_id = g.id
    where c.name ilike %s
       or c.email ilike %s
       or p.phone ilike %s
    group by c.id, g.name
    """
    with conn.cursor() as cur:
        pattern = f"%{pattern}%"
        cur.execute(query, (pattern, pattern, pattern))
        return cur.fetchall()


def search_email(pattern):
    query = """
    select c.id, c.name, c.email,
           coalesce(g.name, 'No group'),
           coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    left join phones p on p.contact_id = c.id
    left join groups g on c.group_id = g.id
    where c.email ilike %s
    group by c.id, g.name
    order by c.name
    """
    with conn.cursor() as cur:
        cur.execute(query, (f"%{pattern}%",))
        return cur.fetchall()


def filter_by_group(group):
    query = """
    select c.id, c.name, c.email,
       g.name,
       coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    join groups g on c.group_id = g.id
    left join phones p on p.contact_id = c.id
    where g.name = %s
    group by c.id, g.name
    """
    with conn.cursor() as cur:
        cur.execute(query, (group,))
        return cur.fetchall()


def get_sorted(field):
    if field not in ["name", "birthday", "created_at"]:
        field = "name"

    query = f"""
    select c.id, c.name, c.email,
           coalesce(g.name, 'No group'),
           coalesce(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
    from contacts c
    left join phones p on p.contact_id = c.id
    left join groups g on c.group_id = g.id
    group by c.id, g.name
    order by c.{field}
    """

    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def change_name(old_name, new_name):
    with conn.cursor() as cur:
        cur.execute("update contacts set name=%s where name=%s", (new_name, old_name))
        conn.commit()


def change_phone(name, new_phone):
    with conn.cursor() as cur:
        cur.execute("""
            update phones
            set phone = %s
            where contact_id = (
                select id from contacts where name = %s
            )
        """, (new_phone, name))
        conn.commit()


def move_to_group(name, group):
    with conn.cursor() as cur:
        if group:
            cur.execute("call move_to_group(%s, %s)", (name, group))
        conn.commit()


def delete_contact(value):
    with conn.cursor() as cur:
        cur.execute("call delete_contact(%s)", (value,))
        conn.commit()


def get_paginated(limit, offset):
    with conn.cursor() as cur:
        cur.execute("select * from get_contacts_paginated(%s, %s)", (limit, offset))
        return cur.fetchall()


def paginate_loop():
    limit = 5
    offset = 0
    while True:
        contacts = get_paginated(limit, offset)
        print_contacts(contacts)
        cmd = input("next / prev / quit: ")
        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break


def add_contact_csv(file):
    with conn.cursor() as cur:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                name, phone = row

                if not phone:
                    continue

                cur.execute("select id from contacts where name = %s", (name,))
                result = cur.fetchone()

                if result:
                    cid = result[0]
                else:
                    cur.execute("""
                        insert into contacts(name, email, birthday)
                        values(%s, %s, %s)
                        returning id
                    """, (name, None, None))
                    cid = cur.fetchone()[0]

                cur.execute("""
                    select 1 from phones
                    where contact_id = %s and phone = %s
                """, (cid, phone))

                if not cur.fetchone():
                    cur.execute("""
                        insert into phones(contact_id, phone, type)
                        values(%s, %s, %s)
                    """, (cid, phone, 'mobile'))

        conn.commit()

    print("CSV imported with merge.")


def export_json():
    query = """
    select c.name, c.email, c.birthday, c.created_at,
           (select name from groups g where g.id = c.group_id),
           coalesce(json_agg(json_build_object('phone', p.phone, 'type', p.type))
                    filter (where p.phone is not null), '[]')
    from contacts c
    left join phones p on p.contact_id = c.id
    group by c.id
    """

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

    data = []
    for name, email, birthday, created_at, group, phones in rows:
        data.append({
            "name": name,
            "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "created_at": created_at.isoformat() if created_at else None,
            "group": group,
            "phones": phones
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)


def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        name = c.get("name")
        email = c.get("email")
        birthday = parse_date_safe(c.get("birthday"))
        group = c.get("group")
        phones = c.get("phones")

        with conn.cursor() as cur:
            cur.execute("select id from contacts where name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists (skip/overwrite): ")
                if choice == "skip":
                    continue
                else:
                    cur.execute("delete from contacts where name=%s", (name,))

            cur.execute("""
                insert into contacts(name, email, birthday)
                values(%s,%s,%s)
                returning id
            """, (name, email, birthday))

            cid = cur.fetchone()[0]

            for p in phones or []:
                cur.execute("""
                    insert into phones(contact_id, phone, type)
                    values(%s,%s,%s)
                """, (cid, p['phone'], p['type']))

            if group:
                cur.execute("call move_to_group(%s, %s)", (name, group))

        conn.commit()


def set_email(name, email):
    with conn.cursor() as cur:
        cur.execute("call set_email(%s, %s)", (name, email))
        conn.commit()


def print_contacts(contacts):
    if not contacts:
        print("No contacts.")
        return

    for c in contacts:
        cid, name, email, group, phones = c

        with conn.cursor() as cur:
            cur.execute("""
                select birthday, created_at
                from contacts
                where id=%s
            """, (cid,))
            row = cur.fetchone()

        birthday = format_date(row[0]) if row else "-"
        created = format_date(row[1]) if row else "-"

        print(f"\n[{cid}] {name}")
        print(f"   Email    : {email or '-'}")
        print(f"   Group    : {group}")
        print(f"   Phones   : {phones if phones else '-'}")
        print(f"   Birthday : {birthday}")
        print(f"   Created  : {created}")


def main():
    init_db()

    while True:
        print("\n------- Contacts -------")
        print("1) Display")
        print("2) Add")
        print("3) Import CSV")
        print("4) Search")
        print("5) Change name")
        print("6) Change phone")
        print("7) Delete")
        print("8) Add phone")
        print("9) Move to group")
        print("10) Filter by group")
        print("11) Search by email")
        print("12) Sort")
        print("13) Pagination")
        print("14) Export JSON")
        print("15) Import JSON")
        print("16) Set email")
        print("0) Exit")

        choice = input("Choice: ")

        match choice:
            case "1":
                print_contacts(get_all_contacts())
            case "2":
                add_contact_console()
            case "3":
                add_contact_csv("contacts.csv")
            case "4":
                print_contacts(search(input("Search: ")))
            case "5":
                change_name(input("Old name: "), input("New name: "))
            case "6":
                change_phone(input("Name: "), input("New phone: "))
            case "7":
                delete_contact(input("Value: "))
            case "8":
                add_phone(input("Name: "), input("Phone: "), input("Type(home, work, mobile): "))
            case "9":
                move_to_group(input("Name: "), input("Group: "))
            case "10":
                print_contacts(filter_by_group(input("Group: ")))
            case "11":
                print_contacts(search_email(input("Email: ")))
            case "12":
                print_contacts(get_sorted(input("Sort(name, birthday, created_at): ")))
            case "13":
                paginate_loop()
            case "14":
                export_json()
            case "15":
                import_json()
            case "16":
                name = input("Name: ")
                email = input("Email: ")
                set_email(name, email)
            case "0":
                break

    conn.close()


if __name__ == "__main__":
    main()
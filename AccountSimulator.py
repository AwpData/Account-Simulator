import hashlib
import sqlite3

conn = sqlite3.connect("../pythonProject2/users.db")
cur = conn.cursor()

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS users (
        Username TEXT,
        Password TEXT,
        id INTEGER PRIMARY KEY AUTOINCREMENT);
""")


def create_account(username, password):
    with conn:
        cur.execute("INSERT INTO users (Username, Password) VALUES (?, ?)",
                    (hash_this(username), hash_this(password)))


def username_checker(desired_username):
    return cur.execute("SELECT Username FROM users WHERE Username IS ?",
                       (hash_this(desired_username),)).fetchone() is None


def hash_this(n):
    return hashlib.sha256(n.encode("utf-8")).hexdigest()


def get_credentials():  # strip() removes whitespaces only at the beginning and end
    return [str(input("Enter username: ")).strip(), str(input("Enter password: ")).strip()]


print("Welcome to account simulator!")
while True:
    print("1. Create account")
    print("2. Login")
    print("3. Quit")
    choice = input()
    if choice == "1":
        credentials = get_credentials()
        if username_checker(credentials[0]):
            create_account(credentials[0], credentials[1])
            print("Account successfully created!\n")
        else:
            print("Error! Username already exists!\n")
    elif choice == "2":
        credentials = get_credentials()
        hash_username = hashlib.sha256(credentials[0].encode("utf-8")).hexdigest()
        hash_password = hashlib.sha256(credentials[1].encode("utf-8")).hexdigest()
        with conn:
            try:
                if cur.execute("SELECT username FROM users WHERE username IS ?", (hash_username,)).fetchone()[
                    0] != hash_username \
                        or cur.execute("SELECT password FROM users where password IS ?",
                                       (hash_password,)).fetchone()[0] != hash_password:
                    print("Username or password is wrong!\n")
            except TypeError:
                print("Username or password is wrong!\n")
            else:
                print("Success!")
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Invalid choice, try again\n")

conn.close()

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
    username = hash_this(username)
    password = hash_this(password)
    with conn:
        cur.execute("INSERT INTO users (Username, Password) VALUES (?, ?)",
                    (username, password))


def username_checker(desired_username):
    statement = cur.execute("SELECT Username FROM users WHERE Username IS ?",
                            (hash_this(desired_username),)).fetchone()
    if statement is None:
        return True
    else:
        return False


def hash_this(n):
    m = hashlib.sha256()
    m.update(n.encode("utf-8"))
    return m.hexdigest()


def get_credentials():
    username_ = str(input("Enter username: "))
    username_ = username_.rstrip()
    password_ = str(input("Enter password: "))
    password_ = password_.rstrip()
    return [username_, password_]


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
            print("Account successfully created!")
        else:
            print("Error! Username already exists!")
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
                    print("Username or password is wrong!")
            except TypeError:
                print("Username or password is wrong!")
            else:
                print("Success!")
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Invalid choice, try again")

conn.close()

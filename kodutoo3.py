import mysql.connector
import hashlib
import os

# Ühendan MySQL-ga
mydb = mysql.connector.connect(
  host="sql7.freemysqlhosting.net",
  user="sql7622597",
  password="aPtgpjsz8b",
  database="sql7622597"
)

# Loon tabeli kus hoida kasutajanimesid ja paroole
def create_table():
    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, kasutaja VARCHAR(255), password VARCHAR(255))")

# Register a new user
def registeeri():
    kasutaja = input("Sisesta kasutajanimi: ")
    password = input("Sisesta parool: ")

    # Soolan parooli
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

    cursor = mydb.cursor()
    insert_query = "INSERT INTO users (kasutaja, password) VALUES (%s, %s)"
    user_data = (kasutaja, hashed_password)
    cursor.execute(insert_query, user_data)
    mydb.commit()

    print("Registreerimine oli edukas!")

# Log in
def logi_sisse():
    kasutaja = input("Sisesta kasutaja: ")
    password = input("Sisesta parool: ")

    cursor = mydb.cursor()
    select_query = "SELECT password FROM users WHERE kasutaja = %s"
    cursor.execute(select_query, (kasutaja,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        # Hash the input password with the same salt and check for a match
        salt = bytes.fromhex(hashed_password[:32])
        input_hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

        if hashed_password == salt.hex() + input_hashed_password:
            print("Sisselogimine edukas!")
        else:
            print("Vale kasutaja või parool.")
    else:
        print("Vale kasutaja või parool.")

# Loon tabeli
create_table()

choice = input("Sisesta '1' et registeerida, '2' et sisse logida: ")

if choice == "1":
    registeeri()
elif choice == "2":
    logi_sisse()
else:
    print("Vale valik.")
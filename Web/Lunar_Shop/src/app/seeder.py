import sqlite3
import json


def create_tables():
    products_query = f'''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        price TEXT NOT NULL
    );'''

    flag_query = f'''CREATE TABLE IF NOT EXISTS flag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flag TEXT NOT NULL UNIQUE
    );'''

    cursor.execute(products_query)
    cursor.execute(flag_query)

    conn.commit()

def seed_products():
    products = json.load(open("products.json"))
    for key, value in products.items():
        print(value)
        cursor.execute(
            "INSERT OR IGNORE INTO products (name, description, price) VALUES (?, ?, ?)",
            (value['name'], value['description'], value['price'])
        )
        conn.commit()


def seed_flag():
    FLAG = open("flag.txt", 'r').read()
    cursor.execute(
        "INSERT OR IGNORE INTO flag (flag) VALUES (?)",
        (FLAG,)
    )
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    create_tables()
    seed_products()
    seed_flag()

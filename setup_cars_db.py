"""

File created: 2025-01-29
Last updated: 2025-02-12
"""

import sqlite3

DATABASE = "cars.db"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS cars (id INT PRIMARY KEY, owner text NOT NULL, previous_owner, price INT NOT NULL);"
CREATE_CAR = "INSERT INTO cars(id, owner, previous_owner, price) VALUES(1337, ?, NULL, 1000000);"


if __name__ == "__main__":
    with open("ACCOUNTS.txt", "r") as f:
        account = f.readlines()[1]

    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()

        cursor.execute(CREATE_TABLE)
        sql.commit()

        cursor.execute(CREATE_CAR, (account, ))
        sql.commit()

    print("OK!")

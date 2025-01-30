"""

File created: 2025-01-29
Last updated: 2025-01-30
"""

import sqlite3

DATABASE = "accounts.db"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS accounts (address text PRIMARY KEY, balance INT NOT NULL);"

if __name__ == "__main__":
    with sqlite3.connect(DATABASE) as sql:
        cursor = sql.cursor()
        cursor.execute(CREATE_TABLE)
        sql.commit()
        print(f"Table `accounts` created successfully in file `{DATABASE}`")
    print("Done!")





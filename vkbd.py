import sqlite3


def add_column():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute(""" 
     
        ALTER TABLE players
        ADD is_on_rest INTEGER DEFAULT 0
     
     """)

    con.commit()
    con.close()


def create_table():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute("""
        
        CREATE TABLE players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER)
            
    
    """)

    con.commit()
    con.close()


def delete_table():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute("""
    
    DROP TABLE players_time
    
    
    """)

    con.commit()
    con.close()


def add_new_user(vk_id):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute("""
        
            INSERT INTO players
            (vk_id, money)
            VALUES
            (?, 0) """, [vk_id])

        con.commit()
        con.close()

    except sqlite3.IntegrityError:
        con.commit()
        con.close()


def add_car(name, price):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute("""

            INSERT INTO cars
            (name, price)
            VALUES
            (?, ?) """, [name, price])

    con.commit()
    con.close()


def check_is_new(vk_id):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute(f"SELECT * FROM players WHERE vk_id={vk_id}")
    row = cur.fetchone()
    print(str(row))

    con.commit()
    con.close()

    return row


def delete_row(vk_id):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute(f"DELETE FROM players WHERE vk_id={vk_id}")

    con.commit()
    con.close()


def change_row(vk_id, par, new):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute(f"""UPDATE players SET {par} = {new} WHERE vk_id = {vk_id} """)

    con.commit()
    con.close()


def get_row(vk_id, par):

    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    cur.execute(f""" SELECT {par} FROM players WHERE vk_id={vk_id} """)

    result = cur.fetchone()[0]

    return result


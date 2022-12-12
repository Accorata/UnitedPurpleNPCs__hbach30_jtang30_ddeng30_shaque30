'''
UnitedPurpleNPCs: Henry, Shafiul, David, Jeffery
SoftDev
P1 -- LoveCalc But Creepy
2022-12-08
time spent: 1 hrs
'''

import sqlite3

DB_FILE = "p1_info.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS info(username TEXT UNIQUE, password TEXT, city TEXT, weather TEXT, temperature INTEGER,
 love_percent INTEGER)""")
'''
UnitedPurpleNPCs: Henry, Shafiul, David, Jeffery
SoftDev
P1 -- LoveCalc But Creepy
2022-12-08
time spent: 1 hrs
'''

from flask import Flask, session, render_template, redirect, url_for, request as flask_request
from db import *
from urllib import *
import http.client
import urllib.request
import sqlite3
import json
import os

DB_FILE = "p1_info.db"
db_name = "p1_info.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS info(username TEXT, city TEXT, weekday TEXT, weather TEXT, temperature INTEGER,
 town TEXT, cont TEXT, country TEXT, abbr TEXT, time TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS love(username TEXT, m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER, m6 INTEGER)""")

def delete_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("delete from info where username = ?;", (username,))
    db.commit()
    db.close()

def delete_user_love(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("delete from info where username = ?;", (username,))
    db.commit()
    db.close()

def store_data(stored_data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("insert into info values (?,?,?,?,?,?,?,?,?,?);", stored_data)
    db.commit()
    db.close()

def store_love_data(stored_data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("insert into love values (?,?,?,?,?,?,?);", stored_data)
    db.commit()
    db.close()

def get_users():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userlist = c.execute("SELECT username from users;").fetchall()
    db.commit()
    db.close()
    return userlist

def get_combo():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    combolist = c.execute("SELECT username, password from users;").fetchall()
    db.commit()
    db.close()
    return combolist

def get_everything():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    combolist = c.execute("SELECT username, city, weekday, weather, temperature, town, cont, country, abbr, time from info;").fetchall()
    db.commit()
    db.close()
    return combolist

def replace(stored_data, user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    delete_user(user)
    store_data(stored_data)
    db.commit()
    db.close()

def replace_love(stored_data, user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    delete_user_love(user)
    store_love_data(stored_data)
    db.commit()
    db.close()

def new_user(new_account):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", new_account)
    db.commit()
    db.close()

def check_user_exist(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (username,))

    user = c.fetchone()
    db.close()

    return user!= None

def change_pw(username, new_pw):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE users SET password = ? WHERE username=?", (new_pw, username))

    db.commit()
    db.close()

def get_ip():
    return flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)

def find_similar_results(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    user_data = get_user_data(username)
    (username, city, weekday, weather, temp, town, cont, country, abbr, time) = user_data
    user_list = c.execute("select * from info where city = ? or weekday = ? or weather = ? or cont = ? or country = ? or abbr = ? or time = ?;", (city, weekday, weather, cont, country, abbr, time)).fetchall()
    user_list_without = []
    for user in user_list :
        if user[0] != username :
            user_list_without += user
    return user_list_without

def get_user_data(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    return c.execute("select * from info where username = ?;", (username,)).fetchone()
    db.commit()
    db.close()

def get_love_user_data(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    return c.execute("select * from love where username = ?;", (username,)).fetchone()
    db.commit()
    db.close()

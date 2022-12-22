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
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS info(username TEXT, city TEXT, weather TEXT, temperature INTEGER,
 time TEXT)""")

def delete_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("delete from info where username = ?;", (username,))
    db.commit()
    db.close()

def store_data(stored_data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("insert into info values (?,?,?,?,?);", stored_data)
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

def get_user_info():
    url = f"https://api.ipify.org"
    data = request.urlopen(url).read()
    ip = str(data)[2:-1]

    ipstack_key = open("app/keys/ipstack_key.txt", "r").read()

    url = f"http://api.ipstack.com/"+ip+"?access_key="+ipstack_key
    print(url)

    data = request.urlopen(url).read()
    location_results = json.loads(data)

    latitude = location_results['latitude']
    longitude = location_results['longitude']

    weatherbit_key = open("app/keys/weatherbit_key.txt", "r").read()

    url = f"http://api.weatherbit.io/v2.0/current?lat="+str(latitude)+"&lon="+str(longitude)+"&key="+weatherbit_key

    data = request.urlopen(url).read()
    weather_results = json.loads(data)['data'][0]
    #return weather_results;
    weather_description = weather_results['weather']['description']
    location = weather_results['timezone']
    divider_index = location.index('/')
    city = location[divider_index+1:]
    #return weather_results

    url = f'https://worldtimeapi.org/api/timezone/'+location+'.json'
    data = request.urlopen(url).read()
    time_results = json.loads(data)
    time_data = time_results['datetime']

    days_of_week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    week_day = days_of_week[int(time_results['day_of_week'])]

    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month = months[int(time_data[5:7])-1]

    day = time_data[8:10]
    year = time_data[0:4]
    time = time_data[11:16]
    return (ip, month+" "+day+", "+year, time, week_day, weather_description, city)

def get_ip():
    return flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)

def find_similar_results(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user_data = c.execute("select * from info where username = ?;", (username,)).fetchone()
    (username, city, weather, temp, number) = user_data
    user_list = c.execute("select * from info where city = ? or weather = ? or temperature = ? or time = ?;", (city, weather, temp, number)).fetchall()
    return user_list

def lovecalc(name1, name2):
    conn = http.client.HTTPSConnection("love-calculator.p.rapidapi.com")
    headers = {
    'X-RapidAPI-Key': "c323d31791msh2d75f0f06146040p12028ajsn5bc1193dd201",
    'X-RapidAPI-Host': "love-calculator.p.rapidapi.com"
    }
    conn.request("GET", "/getPercentage?sname=" + name1 + "&fname=" + name2, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

db.commit()
db.close()

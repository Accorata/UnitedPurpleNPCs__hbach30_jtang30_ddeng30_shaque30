'''
UnitedPurpleNPCs: Henry, Shafiul, David, Jeffery
SoftDev
P1 -- LoveCalc But Creepy
2022-12-08
time spent: 1 hrs
'''


from flask import Flask, session, render_template, redirect, url_for, request as flask_request
from db import *
import urllib.request as request
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

db_name = "p1_info.db"

@app.route('/', methods = ['GET', 'POST']) # Landing Page
def show_index():
    if 'username' not in session :
        return render_template('main.html')
    username = session['username']
    try :
        (ip, date, time, week_day, weather, city, town, continent, country, abbr) = get_user_info()
    except :
        return render_template('index.html', username=username, error="Unfortunately, one of the APIs this site relies on is currently down. We apologize for the error. Please try again later.")
    stored_data = (username, city, week_day, weather, 5, town, continent, country, abbr, time)
    replace(stored_data, username)
    others = find_similar_results(session['username'])
    return render_template('index.html', username=username, ip=ip, date=date, time=time, weekday=week_day, weather=weather, similar=others)#, month=month)

@app.route('/results', methods = ["GET", "POST"])
def show_results():
    if 'username' not in session :
        redirect(url_for('show_index'))
    username = session['username']
    bruh = get_user_data(username)
    stored_data = match(bruh)
    (user, x1, x2, x3, x4, x5, x6) = stored_data
    replace_love(stored_data, username)
    return render_template('results.html', username=username, x1=x1, x2=x2, x3=x3, x4=x4, x5=x5, x6=x6)

@app.route('/signup', methods = ["GET", "POST"]) # Sign up page
def show_signup():
    return render_template('signup.html')

@app.route('/login', methods = ["GET", "POST"]) # Login page
def show_login():
    return render_template('login.html')

@app.route('/new_account', methods = ["POST"])
def create_user():
    if flask_request.method == 'POST':
        db = sqlite3.connect(db_name)
        c = db.cursor()
        user_list = get_users()
        #print(user_list)
        username = flask_request.form['username']
        if check_user_exist(username):
            return render_template('signup.html', error = "Username already exists.")
        if flask_request.form['password'] != flask_request.form['password1']:
            return render_template('signup.html', error = "Passwords do not match.")
        if len(flask_request.form['password']) == 0:
            return render_template('signup.html', error = "Please enter a password.")

        new_account = [username, flask_request.form['password']]
        new_user(new_account)
        session['username'] = username
        return redirect(url_for('show_index'))
    return "Error- not post"

@app.route('/login_user', methods = ["POST"]) # Redirection to home page upon successful login
def login():
    if flask_request.method == 'POST':
        db = sqlite3.connect(db_name)
        c = db.cursor()
        user_list = get_users()
        pw_list = get_combo()
        username = flask_request.form['username']
        pw = flask_request.form['password']
        if check_user_exist(username) == False:
            return render_template('login.html', error = "Username not found. Please create an account or try again.")
        if (username, pw) not in pw_list:
            return render_template('login.html', error = "Incorrect password for this username. Please try again.")
        session['username'] = username
        #print("check")
        return redirect(url_for('show_index'))
    return "Error- not post"

@app.route('/logout', methods = ["POST"])
def logout():
    session.pop('username')
    return redirect(url_for('show_index'))


######################


def get_user_info():
    url = "https://api.ipify.org"
    data = request.urlopen(url).read()
    ip = str(data)[2:-1]

    ipstack_key = open("app/keys/ipstack_key.txt", "r").read()
    url = f"http://api.ipstack.com/"+ip+"?access_key="+ipstack_key

    data = request.urlopen(url).read()
    location_results = json.loads(data)
    continent = location_results['continent_name']
    country = location_results['country_name']
    town = location_results['city']

    latitude = location_results['latitude']
    longitude = location_results['longitude']


    weatherbit_key = open("app/keys/weatherbit_key.txt", "r").read()
    url = "https://api.weatherbit.io/v2.0/current?lat="+str(latitude)+"&lon="+str(longitude)+"&key="+weatherbit_key
    data = request.urlopen(url).read()

    weather_results = json.loads(data)['data'][0]
    weather_description = weather_results['weather']['description']
    location = weather_results['timezone']
    divider_index = location.index('/')
    city = location[divider_index+1:]
    city = city.replace("_", " ")

    url = f'https://worldtimeapi.org/api/timezone/'+location+'.json'
    data = request.urlopen(url).read()
    time_results = json.loads(data)
    time_data = time_results['datetime']
    abbr = time_results['abbreviation']

    days_of_week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    week_day = days_of_week[int(time_results['day_of_week'])]

    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month = months[int(time_data[5:7])-1]
    day = time_data[8:10]
    year = time_data[0:4]
    time = time_data[11:16]
    print (ip, month+" "+day+", "+year, time, week_day, weather_description, city, town, continent, country, abbr)
    return (ip, month+" "+day+", "+year, time, week_day, weather_description, city, town, continent, country, abbr)

def lovecalc(name1, name2):
    name1 = name1.replace(' ', "%20")
    name2 = name2.replace(' ', "%20")
    conn = http.client.HTTPSConnection("love-calculator.p.rapidapi.com")
    headers = {
    'X-RapidAPI-Key': "c323d31791msh2d75f0f06146040p12028ajsn5bc1193dd201",
    'X-RapidAPI-Host': "love-calculator.p.rapidapi.com"
    }
    conn.request("GET", "/getPercentage?sname=" + name1 + "&fname=" + name2, headers=headers)
    res = conn.getresponse()
    data = res.read()
    da = json.loads(data)
    return da

def match(bruh):
    x1 = (lovecalc(bruh[0], bruh[1]))['percentage']
    x2 = (lovecalc(bruh[2], bruh[3]))['percentage']
    x3 = (lovecalc(bruh[1], bruh[3]))['percentage']
    x4 = (lovecalc(bruh[1], bruh[5]))['percentage']
    x5 = (lovecalc(bruh[1], bruh[6]))['percentage']
    x6 = (lovecalc(bruh[1], bruh[7]))['percentage']
    stored_data = (bruh[0], x1, x2, x3, x4, x5, x6)
    return stored_data

if __name__ == "__main__":
    app.debug = True
    app.run()

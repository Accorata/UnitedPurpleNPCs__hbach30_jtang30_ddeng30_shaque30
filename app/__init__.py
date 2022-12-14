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
import urllib.request
import sqlite3
import json
import os



app = Flask(__name__)
app.secret_key = os.urandom(32)


db_name = "app/p1_info.db"



@app.route('/', methods = ['GET', 'POST']) # Landing Page
def show_index():
    if 'username' not in session :
        return render_template('main.html')

    username = session['username']

    # Time from location (I'll move this to a seperate function soon)

    ipstack_key = open("app/keys/ipstack_key.txt", "r").read()

    url = f"https://api.ipify.org" # ***** We need to make an kb for this
    data = request.urlopen(url).read()
    ip = str(data)[2:-1]
    # return ip

    url = f"http://api.ipstack.com/"+ip+"?access_key="+ipstack_key

    data = request.urlopen(url).read()
    location_results = json.loads(data)

    latitude = location_results['latitude']
    longitude = location_results['longitude']

    weatherbit_key = open("app/keys/weatherbit_key.txt", "r").read()

    url = f"https://api.weatherbit.io/v2.0/current?lat="+str(latitude)+"&lon="+str(longitude)+"&key="+weatherbit_key

    data = request.urlopen(url).read()
    weather_results = json.loads(data)['data'][0]
    #return weather_results;
    weather_descption = weather_results['weather']['description']
    location = weather_results['timezone']

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

    #return results
    return render_template('index.html', username=username, ip=ip, date=month+" "+day+", "+year, time=time, weekday=week_day, weather=weather_descption)#, month=month)


@app.route('/signup', methods = ["GET", "POST"]) # Sign up page
def show_signup():
    return render_template('signup.html')


@app.route('/login', methods = ["GET", "POST"]) # Login page
def show_login():
    return render_template('login.html')


@app.route('/new_account', methods = ["POST"])
def create_account():
    if flask_request.method == 'POST':
        db = sqlite3.connect(db_name)
        c = db.cursor()
        user_list = c.execute("SELECT username from users;").fetchall()
        #print(user_list)
        if (flask_request.form['username'],) not in user_list: 
            username = flask_request.form['username']
            new_account = [username, flask_request.form['password']]
            c.execute("INSERT INTO users VALUES (?, ?)", new_account)
            db.commit()
            db.close()
            session['username'] = username
            return redirect(url_for('show_index'))
        return render_template('signup.html', error = "Username already exists")
    return redirect(url_for('show_index'))


@app.route('/login_user', methods = ["POST"]) # Redirection to home page upon successful login
def login():
    #login stuff
    return redirect(url_for('show_index'))


@app.route('/logout', methods = ["POST"])
def logout():
    session.pop('username')
    return redirect(url_for('show_index'))


def get_ip():
    return flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)

if __name__ == "__main__":
    app.debug = True
    app.run()
    
def find_similar_results():
    return 100

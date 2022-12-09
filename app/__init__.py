'''
UnitedPurpleNPCs: Henry, Shafiul, David, Jeffery
SoftDev
P1 -- LoveCalc But Creepy
2022-12-08
time spent: 1 hrs
'''


from flask import *
from db import *
from urllib import *
import sqlite3
import json

app = Flask(__name__)
# key = open("key_nasa.txt", "r").read()

db_name = "discobandit.db"

# db = sqlite3.connect(db_name)
#     c = db.cursor()
#     db.close()

@app.route('/') # Landing Page
def show_index():
    # url = request.urlopen(f"https://api.nasa.gov/planetary/apod?api_key={key}").read()
    # dict = json.loads(url)
    # , picture=dict['url'], explanation=dict['explanation'], head = dict['title']

    # Time from location (I'll move this to a seperate function soon)

    #ipstack_key = open("key_nasa.txt", "r").read()

    location = 'America/New_York'

    url = f'https://worldtimeapi.org/api/timezone/'+location+'.json'
    data = request.urlopen(url).read()
    results = json.loads(data)
    time_data = results['datetime']

    days_of_week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    week_day = days_of_week[int(results['day_of_week'])]

    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month = months[int(time_data[5:7])-1]

    day = time_data[8:10]
    year = time_data[0:4]
    time = time_data[11:16]

    #return results
    return render_template('index.html', date=month+" "+day+", "+year, time=time, weekday=week_day)#, month=month)

    # if 'username' in session :
    #     return render_template('index.html')
    # else :
    #     return render_template('main.html')

@app.route('/signup') # Sign up page
def show_signup():
    return render_template('signup.html')

@app.route('/login') # Login page
def show_login():
    return render_template('login.html')

@app.route('/new_account')
def create_account():
    #...
    return redirect(url_for('show_index'))

@app.route('/login_user') # Redirection to home page upon successful login
def login():
    #login stuff
    return redirect(url_for('show_index'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('show_index'))

if __name__ == "__main__":
    app.debug = True
    app.run()

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
    
    #return render_template('index.html')

    location = 'America/New_York'
    url = f'https://worldtimeapi.org/api/timezone/'+location+'.json'
    data = request.urlopen(url).read()
    results = json.loads(data)

    time_data = results['datetime']
    time = time_data[10:]
    return time
    #time = results[something]

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

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
        (ip, date, time, week_day, weather, city) = get_user_info()
    except :
        return render_template('index.html', username=username, error="Unfortunately, one of the APIs this site relies on is currently down. We apologize for the error. Please try again later.")
    stored_data = (username, city, weather, 5, time)
    db = sqlite3.connect(db_name)
    c = db.cursor()
    delete_user(username)
    store_data(stored_data)
    others = find_similar_results(session['username'])
    return render_template('index.html', username=username, ip=ip, date=date, time=time, weekday=week_day, weather=weather)#, month=month)

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

if __name__ == "__main__":
    app.debug = True
    app.run()

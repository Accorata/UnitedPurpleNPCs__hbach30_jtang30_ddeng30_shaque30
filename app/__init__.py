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

@app.route('/')
def showindex():
    # url = request.urlopen(f"https://api.nasa.gov/planetary/apod?api_key={key}").read()
    # dict = json.loads(url)
    # , picture=dict['url'], explanation=dict['explanation'], head = dict['title']
    return render_template('index.html')

    # if 'username' in session :
    #     return render_template('index.html')
    # else :
    #     return render_template('login.html')



if __name__ == "__main__":
    app.debug = True
    app.run()

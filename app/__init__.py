from flask import *
from db import *
from urllib import *
import sqlite3
import json

app = Flask(__name__)
# key = open("key_nasa.txt", "r").read()

@app.route('/')
def showindex():
    # url = request.urlopen(f"https://api.nasa.gov/planetary/apod?api_key={key}").read()
    # dict = json.loads(url)
    # , picture=dict['url'], explanation=dict['explanation'], head = dict['title']
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
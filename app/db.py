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

c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS info(username TEXT, city TEXT, weather TEXT, temperature INTEGER,
 time TEXT)""")

def delete_user(username):
    return c.execute("delete from info where username = ?;", (username,))

def store_data(stored_data):
    return c.execute("insert into info values (?,?,?,?,?);", stored_data)

def get_users():
    return c.execute("SELECT username from users;").fetchall()

def get_combo():
    return c.execute("SELECT username, password from users;").fetchall()

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
    db = sqlite3.connect(db_name)
    c = db.cursor()
    user_data = c.execute("select * from info where username = ?;", (username,)).fetchone()
    (username, city, weather, temp, number) = user_data
    user_list = c.execute("select * from info where city = ? or weather = ? or temperature = ? or time = ?;", (city, weather, temp, number)).fetchall()
    return user_list

db.commit()
db.close()
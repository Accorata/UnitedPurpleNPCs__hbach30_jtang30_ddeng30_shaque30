# Stalker by UnitedPurpleNPCs
## PM: Henry Bach (API/Flask)
## Devo: Jeffery Tang (SQLite)
## Devo: David Deng (API/Flask)
## Devo: Shafiul Haque (HTML)

## Summary

Our plan is to create a website that demonstrates the information we can retrieve from the user without their consent. Once users log in, they'll be able to see their location, weather, time, and a list of percentages attached to various predictions.

In addition, the website will store all this information in a database. This way, when the current user wishes, the website will display similar results from previous users. 

## APIs
- IPify API: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_ipify.md 
- Love Calculator API: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_LoveCalculator.md
- ipstack API: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_ipstack.md
- WorldTimeAPI: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_WorldTimeAPI.md
- WeatherBit API: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_weatherAPI.md

## How to Clone, Install, and Run

`0) Create and activate an environment`
```
python3 -m venv <<name>>
cd <<name>>
. bin/activate
```
`1) Clone the project `
```
git clone git@github.com:Accorata/UnitedPurpleNPCs__hbach30_jtang30_ddeng30_shaque30.git
```

`2) Navigate to root directory`

``` 
cd UnitedPurpleNPCs__hbach30_jtang30_ddeng30_shaque30/
```
`3) install requirements`
```
pip install -r requirements.txt
```
`4) Run the program`

``` 
python3 app/__init__.py
```

`5) Open the following link in any web browser`
```
https://127.0.0.1:5000

#!/usr/bin/python
import sys, ConfigParser, json, time, Adafruit_DHT, datetime, signal
from urllib import urlopen
from pymongo import MongoClient

DB_HOST = configParser.get('DATABASE', 'DB_HOST')
DB_PORT = configParser.getint('DATABASE', 'DB_PORT')
DB_NAME = configParser.get('DATABASE', 'DB_NAME')
DB_USER = configParser.get('DATABASE', 'DB_USER')
DB_PASS = configParser.get('DATABASE', 'DB_PASS')
DB_COLL = configParser.get('DATABASE', 'DB_COLL')
MY_LAT = configParser.getfloat('LOCATION', 'MY_LAT')
MY_LON = configParser.getfloat('LOCATION', 'MY_LON')
OPEN_WEATHER_KEY = configParser.get('APIKEYS', 'OPEN_WEATHER_KEY')

def signal_handler(signal, frame):
  print("\nprogram exiting")
  # f.close()
  # db.close()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

connection = MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)
collection = db[DB_COLL]

# path = '/home/pi/Documents/Maria/humidity/sensor_data.txt'
# f = open(path, 'a')

api = "http://api.openweathermap.org/data/2.5/weather?"
lat = "lat=" + str(MY_LAT)
lon = "lon=" + str(MY_LON)
units = "units=" + 'metric'
apikey = "OPEN_WEATHER_KEY"
urlString = ''.join([api, lat, "&", lon, "&appid=", apikey, "&", units])

while True:
  outdoorWeather = json.loads(urlopen(urlString).read())
  outdoorTemp = outdoorWeather['main']['temp']
  outdoorHumidity = outdoorWeather['main']['humidity']
  humidity, temperature = Adafruit_DHT.read_retry(11, 4)
  now = datetime.datetime.utcnow()
  data = 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
  # f.write(now.strftime('%c') + ' ' + data + '\n')
  print now, data, outdoorTemp, outdoorHumidity
  reading = {"temp": temperature,
            "humidity" : humidity,
            "outdoorTemp" : outdoorTemp,
            "outdoorHumidity" : outdoorHumidity,
            "date": now }
  collection.insert(reading)
  time.sleep(14400)

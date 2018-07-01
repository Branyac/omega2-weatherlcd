#!/usr/bin/env python
import json
import lcdDriver
import time
import urllib
import urllib2

lcdAddress = 0x27
woeid = "753692"		# Barcelona, Spain
changeInfoSecs = 10
maxLoops = 300 / changeInfoSecs	# Update weather info every 5 minutes

api_url = "https://query.yahooapis.com/v1/public/yql?"
api_query = "select units,location,atmosphere,item from weather.forecast where woeid=" + woeid + " and u='c'"
yql_url = api_url + urllib.urlencode({'q':api_query}) + "&format=json"

# setup LCD
lcd = lcdDriver.Lcd(lcdAddress)
lcd.backlightOn()

while 1==1:
	lcd.lcdClear()
	lcd.lcdDisplayStringList(['', 'Fetching Yahoo Weather data...'])

	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)

	results = data['query']['results']['channel']
	location = results['location']
	condition = results['item']['condition']
	atmosphere = results['atmosphere']
	units = results['units']
	forecast = results['item']['forecast'][0]
	
	for loop in range(0,maxLoops):
		lcd.lcdClear()
		lcd.lcdDisplayStringList([
			location['city'] + ', ' + location['country'],
			'Max.: ' + forecast['high']  + units['temperature'] + ' Min.: '  + forecast['low']  + units['temperature'],
			'Now => Temp:' + condition['temp'] + units['temperature'],
			'    => Presure:' + atmosphere['humidity'] + units['pressure']
		])
		time.sleep(changeInfoSecs);

		lcd.lcdClear()
		lcd.lcdDisplayStringList([
			location['city'] + ', ' + location['country'],
			'Forecast: ' + forecast['text'],
			'Now => ' + condition['text']
		])
		time.sleep(changeInfoSecs);

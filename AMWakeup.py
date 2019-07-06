import console
import ui
import dialogs
import datetime
import location
import speech
import requests
import webbrowser
import random

def get_temperature():
	location.start_updates()
	latlong = location.get_location()
	coordinates = {"latitude": latlong["latitude"], "longitude": latlong["longitude"]}
	geo = location.reverse_geocode(coordinates)
	api_call = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=apiKey".format(coordinates['latitude'],coordinates['longitude'])
	weather = requests.get(api_call)
	response = weather.json()
	temperature = round(1.8*(response['main']['temp'] -273) + 32, 2)
	description = response['weather'][0]['description']
	if description == "overcast clouds":
		speech.say("It appears to be a bit cloudy today", "en-UK")
		speech.say("The current temperature outside is {} degrees".format(temperature),"en-UK")
	elif description == "broken clouds":
		speech.say("Looks like some broken clouds today", "en-UK")
		speech.say("The current temperature outside is {} degrees".format(temperature), "en-UK")
	elif description == "moderate rain":
		speech.say("Appears to be a wet one today, might want to take an umbrella", "en-UK")
		speech.say("The current temperature outside is {} degrees".format(temperature), "en-UK")
	elif description == "light rain":
		speech.say("Appears there will be some light rain, might want to take an umbrella", "en-UK")
		speech.say("The current temperature outside is {} degrees".format(temperature), "en-UK")
	elif description == "clear sky":
		speech.say("Clear skies out right now, looks like a good way to start the day", "en-UK")
		speech.say("The current temperature outside is {} degrees".format(temperature), "en-UK")
	else:
		speech.say("Not sure you gave me enough code, you may need to add to my code base", "en-UK")
	
def top_headline():
	news_api = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=")
	news_response = news_api.json()
	top_headline = news_response['articles'][0]['description']
	author = news_response['articles'][0]['author']
	source = news_response['articles'][0]['source']['id']
	speech.say("Your top headline for this morning comes by way of author {}. {}".format(author, top_headline),"en-UK")
	
def sports_headline():
	api = requests.get("https://newsapi.org/v2/everything?q=NFL&apiKey=")
	sports_response = api.json()
	top_sports_headline = sports_response['articles'][0]['description']
	author = sports_response['articles'][0]['author']
	source = sports_response['articles'][0]['source']['id']
	speech.say("Your top sports headline for this morning comes by way of {}. {}".format(source, top_sports_headline),"en-UK")
	sports_url = sports_response['articles'][0]['url']

def random_greetings():
	greetings = ["Good Morning Mr. {Name}", "Rise and Shine Mr.{Name}, time to get moving", "Perhaps you should try spending less time sleeping and more time moving", "Quite frankly Mr. {Name} 5 hours of sleep is good enough.", "Mr. {Name} if you sleep any longer your eyes may get stuck in a closed position"]
	morning_greeting = random.choice(greetings)
	speech.say(morning_greeting, "en-UK")

def get_reminders_today():
	import reminders
	import re
	calendar = reminders.get_reminders()
	reminder_1 = re.findall(r'"(.*?)"', str(calendar[0]))
	speech.say("On your reminders list was {}, not sure how important that is, but nevertheless you might want to look into it. I've taken the liberty to send you a text message regarding this. Just a gentle reminder to take care of your stuff today.".format(str(reminder_1[0])), "en-UK") 
	options = {"value1": reminder_1[0]}
	requests.post("https://maker.ifttt.com/trigger/Calendar/with/key/{IFTT Key Goes Here}", options)
	
def anything_else():
	import time, sound
	speech.say("Mr. {Name} is there anything else I may help you with?", "en-UK")
	time.sleep(3)
	rec = sound.Recorder("audio.m4a")
	rec.record()
	time.sleep(3)
	rec.stop()
	result = speech.recognize("audio.m4a")[0][0]
	if result == "Yes":
		speech.say("Oops that is the end of my code sir, but I did hear yes", "en-UK")
	elif result == "No":
		speech.say("That is the end of my code sir, but I did hear no.", "en-UK")
	else:
		speech.say("I did not hear a response, so I will assume you are ready for the day,", "en-UK")
		
random_greetings()	
get_temperature()
top_headline()
sports_headline()
get_reminders_today()
anything_else()

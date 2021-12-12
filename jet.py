# Hi, this is JET!
# Your personal virtual assistant!!

''' JET can do all of the following:

1. tell the date
2. tell the time
3. random greeting!
4. return information about a famous character! '''

# Needed packages:
# pip install Pyaudio
# pip install SpeechRecognition
# pip install gTTs
# pip install wikipedia

# Importing all the required libraries

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import random
import calendar
import wikipedia

# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return it as a string (function)
def recordAudio():
    # Record:
    r = sr.Recognizer() # recognizer object

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Say Something . . . ")
        audio = r.listen(source)

    # Use Google's speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError: # check for unkown errors
        print("Google Speech Recognition cannot understand what you just said, unkown error")
    except sr.RequestError as e:
        print("Request results from google speech recognition service error: " + e)

    return data

# Get assistant response

def assistantResponse(text):
    print(text)
    # Convert the text to speech
    myobj = gTTS(text = text, lang = "en", slow = False)
    # Save the response audio as a file
    myobj.save("assistant_response.mp3")
    # Play the converted file
    os.system("start assistant_response.mp3")


# Wake word(s)
def wakeWords(text):
    WAKE_WORDS = ["hello jet", "hi jet", "jet", "hi", "hello"]
    text = text.lower()
    for word in WAKE_WORDS:
        if word in text:
            return True
    return False

# Return current date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] # name of the day
    monthNum = now.month
    dateNum = now.day

    # A list of months
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]

    # A list of ordinal_numbers
    ordinalNumbers = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
                      "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th",
                      "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th",
                      "29th", "30th", "31st"]

    return "Today is: " + weekday + " " + month_names[monthNum - 1] + " the " + ordinalNumbers[dateNum - 1] + "."

# Random greeting response
def randomGreeting(text):
    # greeting inputs
    GREETING_INPUTS = ["hello", "hi", "hey", "welcome"]
    # greeting responses
    GREETING_RESPONSES = ["hey there", "how are you doing", "wassup", "hi", "hello", "how can i help you"]
    # if the user's input is a greeting word, return a random greeting
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + "."

    # if no greeting word in input return an empty string
    return ""

# get a person's first and last name from a text
def getPerson(text):
    wordList = text.split() # splitting the text into a group of words
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == "who" and wordList[i + 1].lower() == "is":
            return wordList[i + 2] + " " + wordList[i + 3]

# Making an infinite while loop that will keep the program listening all the time
while True:
    # Recording audio
    text = recordAudio()
    response = ""
    # checking for the wake word
    if(wakeWords(text) == True):
        # checking for greetings by the user
        response = response + randomGreeting(text)
        # checking if the user is asking for the date
        if("date" in text):
            get_date = getDate()
            response = response + " " + get_date
        # checking if the user is asking for the time
        if("time" in text):
            now = datetime.datetime.now()
            meridium = ""
            if now.hour < 12:
                meridium = "AM"
                hour = now.hour
            else:
                meridium = "PM"
                hour = now.hour - 12
            # converting minutes into a proper string
            if now.minute < 10:
                minute = "0" + str(now.minute)
            else:
                minute = str(now.minute)
            response = response + " " + "It is " + str(hour) + ":" + minute + " " + meridium
        # checking if person inquiry is activated
        if("who is" in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + " " + wiki
        # virtual assistant response
        assistantResponse(response)

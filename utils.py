import pywhatkit as kit
import requests
import wikipedia
from email.message import EmailMessage
import smtplib
import gtts
import os
from decouple import config
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from kivy.clock import Clock


from constants import (
    EMAIL,
    PASSWORD,
    IP_ADDR_API_URL,
    NEWS_FETCH_API_URL,
    WEATHER_FORECAST_API_URL,
    SMTP_URL,
    SMTP_PORT,
    NEWS_FETCH_API_KEY,
    WEATHER_FORECAST_API_KEY,
)


def speak(text):
    tts = gtts.gTTS(text, lang="en")
    tts.save("output.wav")

    audio = AudioSegment.from_file("output.wav")
    os.remove("output.wav")
    audio = audio.speedup(playback_speed=1.5)

    play(audio)


def find_my_ip():
    ip_addr = requests.get("https://api.ipify.org?format=json").json()
    return ip_addr["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email["To"] = receiver_add
        email["Subject"] = subject
        email["From"] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_news():
    news_headlines = []
    result = requests.get(
        NEWS_FETCH_API_URL,
        params={
            "country": "in",
            "category": "general",
            "apikey": NEWS_FETCH_API_KEY,
        },
    ).json()
    articles = result["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:6]


def weather_forecast(city):
    res = requests.get(
        WEATHER_FORECAST_API_URL,
        params={"q": city, "appid": WEATHER_FORECAST_API_KEY, "units": "metric"},
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"

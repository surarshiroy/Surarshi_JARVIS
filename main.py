import os 
from dotenv import load_dotenv
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from groq import Groq   

load_dotenv()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    


def aiProcess(command):
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": "You are Jarvis, a helpful and witty virtual assistant."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )
    return completion.choices[0].message.content



def processComand(c):
    newsapi = os.getenv("NEWS_API_KEY")
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open my profile" in c.lower() or "open my profile on linkedin" in c.lower():
        webbrowser.open("www.linkedin.com/in/surarshi-roy-705009329")


    elif c.startswith("play"):

        song = c.replace("play ", "").strip()

        if song in musicLibrary.music:

            link = musicLibrary.music[song]

            webbrowser.open(link)

            speak(f"Playing {song}")

        else:

            speak("I couldn't find that song in your library")




    elif "news headlines" in c.lower():
        print("Fetching news...") 
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            
            if not articles:
                speak("I found no news at the moment.")
            
            for article in articles[:5]:
                print(f"Headline: {article['title']}") 
                speak(article['title'])
        else:
            print(f"API Error: {r.status_code}")
            speak("I am having trouble accessing the news right now.")


    else:
        output= aiProcess(c)
        speak(output)

        
if __name__ == "__main__":
    r = sr.Recognizer()
    speak("Initializing Jarvis....")
    
    while True:
        try:
            with sr.Microphone() as source:
                
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=4, phrase_time_limit=3)
            
            
            word = r.recognize_google(audio)
            print(f"I heard: {word}")

            if "jarvis" in word.lower():
                speak("yes")   
                
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    processComand(command)

        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"Error: {e}")
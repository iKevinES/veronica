from gtts import gTTS
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
from playsound import playsound

def speak(audio):
    tts = gTTS(text=audio, lang="es", slow=False)
    audio_file = "query.wav"
    tts.save(audio_file)
    playsound(audio_file)
    os.remove(audio_file)

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("la hora actual es")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("el día actual es")
    speak(date)
    speak(month)
    speak(year) 





def wishme():
    speak("bienvenido de nuevo señor!")
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour <  12:
        speak("buenos días")
    elif hour >=12 and hour < 18:
        speak("buenas tardes")
    elif hour >= 18 and hour <= 24:
        speak("buenas noches")
    else:
        speak("buenas noches")

    speak("veronica a su servicio. cómo puedo ayudarle?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        playsound("sounds/beep_open.wav")
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

    try:
        playsound("sounds/r2d2.wav")
        query = r.recognize_google(audio, language = "es-es")
    except Exception as e:
        print(e)
        speak("repítalo de nuevo porfavor...")

        return "None"
    
    return query

def sendmail(to, content):
    server = smtplib.SMTP('mail.google.com', 587)
    server.ehlo()
    server.starttls()
    server.login("usuario@gmail.com", "contraseña")
    server.sendmail("usuario@gmail.com", to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.jpg")

def pc_state():
    usage = str(psutil.cpu_percent())
    speak("la cpu está en " + usage + "grados")

    battery = psutil.sensors_battery()
    speak("la batería está en")
    speak(battery.percent )

def jokes():
    speak(pyjokes.get_joke(language='es'))

if __name__ == "__main__":

    wishme()

    while True:
        query = takeCommand().lower()

        if "hora" in query:
            time()
        elif "día" in query:
            date()
        elif "salir" in query:
            quit() 
        elif "wikipedia" in query:
            wikipedia.set_lang("es")
            speak("buscando...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            speak("según wikipedia..." + result)
        elif "correo" in query:
            try:
                speak("que quiere enviar?")
                content = takeCommand()
                to = "enviar@a.email"
                sendmail(to, content)
                speak("correo electrónico enviado correctamente")
            except Exception as e:
                speak(e)
                speak("no se puede enviar el mensaje")
        elif "busca en internet" in query:
            speak("qué quiere buscar?")
            firefoxpath  = "/usr/bin/firefox %s"
            search = takeCommand().lower()
            wb.get(firefoxpath).open_new_tab("https://www.qwant.com/?q=" + search)
        
        elif "cierra sesión" in query:
            os.system("gnome-session-quit")

        elif "apaga el aquipo" in query:
            os.system("shutdown now")

        elif "reinicia el equipo" in query:
            os.system("shutdown -r now")

        elif "reproduce música" in query:
            songs_dir = "~/Música"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif "recuérdame algo" in query:
            speak("qué quiere que le recuerde?")
            data = takeCommand()
            speak("de acuerdo, le recordaré que" + data)
            remember = open("reminders.txt", "w")
            remember.write(data)
            remember.close()
        
        elif "olvidado" in query:
            remember = open("reminders.txt", "r")
            speak("me dijo que le recuerde esto:" + remember.read())

        elif "captura de pantalla" in query:
            screenshot()
            speak("listo!")

        elif "estado del equipo" in query:
            pc_state()
        elif "chiste" in query:
            jokes()
        

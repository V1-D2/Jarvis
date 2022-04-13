import os
import asyncio
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import wikipedia                    #Extracts data’s required from Wikipedia
import pyttsx3
from google_trans_new import google_translator
import selenium
from selenium import webdriver
import Weather
from Weather import weatherPl
from Weather import weatherIn
from Weather import weather
import Humor
from Humor import startTheHumorFunctions
import configparser
from telethon.sync import TelegramClient
from telethon import connection
from telethon.tl.functions.messages import GetHistoryRequest
import pyautogui as pg
import Clouses
from Clouses import goToStreet
from Clouses import goToSport
from Clouses import nowIsNotAvailable
from Clouses import nowIsAvailable


# options
opts = {
    "alias": ('джарвис', 'джаз', 'джазз', 'джей', 'джо', 'джас', 'джасс', 'джем'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'произнеси','пожалуйста', 'извини','что такое'),
    "cmds": {
        "wiki":('чекни в википедии', 'посмотри в википедии', 'чекни в вики', 'посмотри в вики', 'посмотри вики', 'осмотри в википедии', 'забей в википедию', 'забей в вики', 'дай опредление'),
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "deliver":('давай закажем еды','закажем еду', 'мы хотим заказать еду', 'закажем', 'давай закажем', 'давай закажем еды','я хочу кушать'),
        "whatTheWeather":('какая погода', 'погода Киев','сколько градусов','сколько влажность','какая температура'),
        "weatherInPlace":('какая погода в','посмотри погоду в ','чекни погоду в','погоду в'),
        "iChangedThePlace":('я переехал в ','теперь я живу в ','сейчас я живу в ', 'я нахожусь в '),
        "humor":("пошути", "расскажи анекдот", "анекдот", "шутку", "пошути"),
        "openGoogle":("открой гугл", "опен гугл", "открой поисковик"),
        "translation":("переведи", "перевести", "сказать перевод", "перевод"),
        "openYouTube":("открой ютуб", "отрыть ютуб", "включи ютуб", "включить ютуб", "на ютубе", "я хочу посмотреть ютуб"),
        "remindPills":("напомни что мне нужно", "что мне нужно принять", "что мне нужно выпить", "какие таблетки мне надо выпить"),
        "addNewPills":("нужно добавить новые таблетки","новые таблетки","добавь к списку таблеток","незабудь добавить к спику таблеток"),
        "deleteSomePells":("удали из списка таблеток","удали из спика","я больше не пью","мне больше не надо принимать"),
        "iAmGoingToEat":("я иду кушать","буду кушать","я буду обедать", "я иду завтракать", "я буду завтракать", "я иду обедать", "я иду ужинать", "я пошёл кушать"),
        "missedMassages":("что я пропустил","есть новые сообщения","мне кто то писал","есть что то новое"),
        "writeTo":("я хочу написать","давай напишем","будем писать","сейчас настрочим"),
        "searchInBrowser":("загугли","посмотри в гугле"),
        "openProgram":("открой ", "открой на компьютере"),
        "writeDown":("запиши", "у меня есть важная идея", "давай запишем идею"),
        "readTheIdeas":("прочитай список идей", "прочитай идеи", "напомни мне мои идеи"),
        "whatToBuy":("запиши что мне нужно купить", "мне нужно купить", "нужно купить"),
        "neededProducts":("скажи что мне нужно купить", "прочитай список продуктов", "прочитай список новых продуктов"),
        "cleanTheMarketList":("очисти список покупок", "я всё купил", "очисти покупки"),
        "forStreet":("что мне одеть на улицу", "подбери что мне одеть", "что мне одеть"),
        "forSport":("я иду тренироваться", "я иду играть", "подбери в чем мне играть", "в чём мне играть", "я иду в зал, что мне", "я иду заниматься"),
        "nowIsAvailable":("опять чистая", "вернулась", "вернулись", "вернулся", "опять чистые", "опять чистый"),
        "nowIsNotAvailable":("теперь в стирке", "пока не доступны", "пока не доступна", "пока не доступный", "теперь в стирки")
    }
}
cmdWithAdditionalInformation = ["nowIsAvailable", "nowIsNotAvailable", "forSport", "whatToBuy", "writeDown", "openProgram","wiki", "searchInBrowser", "weatherInPlace", "iChangedThePlace", "translation", "writeTo", "deleteSomePells"]
placeWhereIAm = "Киев"



''' Things related to listening or speaking '''
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

#Voice engine
speak_engine = pyttsx3.init("sapi5")
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    lastCall = time.clock()

# recognize the answer for additional questions
def listenTheAnswer():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as audio_file:
        speak("Speak Please")

        r.adjust_for_ambient_noise(audio_file)
        audio = r.listen(audio_file)

        return r.recognize_google(audio, language="ru-RU").lower()

''' End '''





''' Functions related to recognition '''

# recognize the command and activate the command
def callbackForCommands(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        cmd = voice
        if(shouldIncludeName()):
            if voice.startswith(opts["alias"]):
                # say hi
                condition()
                cleanRecognizeExecute(cmd)
        else:
            # say hi
            condition()
            cleanRecognizeExecute(cmd)

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def cleanRecognizeExecute(cmd):
    # clean command
    cmd = cleanCMD(cmd)
    # recognize command
    cmd = recognize_cmd(cmd)
    # execute command
    execute_cmd(cmd)


def cleanCMD(cmd):
    for x in opts['alias']:
        cmd = cmd.replace(x, "").strip()

    for x in opts['tbr']:
        cmd = cmd.replace(x, "").strip()

    return cmd

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0, 'startCmd':cmd}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if (cmd["cmd"] in cmdWithAdditionalInformation):
        eval(cmd['cmd']+f'(cleanTheRequest(cmd["startCmd"], cmd["cmd"]))')
    else:
        #print(cmd["cmd"])
        eval(cmd['cmd'] + "()")


def cleanTheRequest(request, cmd):
    s = f'{cmd}'
    for i in range(len(opts['cmds'][s])):
        prhase = opts['cmds'][s][i]
        if(prhase in request):
            request = request.replace(prhase, "").strip()
            return request
    return request[len(opts["cmds"][f'{cmd}'][0]):]

''' End of recognition '''



''' Should J say hi? '''
def condition():
    global lastCallx
    timePassed = time.clock() - lastCall
    if(timePassed > 3600):
        hourNow = int(time.strftime("%H", time.localtime()))
        grettMe()

def shouldIncludeName():
    global lastCall
    timePassed = time.clock() - lastCall
    if (timePassed > 3600):
        return True
    else:
        return False

def grettMe():
    hour = int(time.strftime("%H", time.localtime()))
    if hour>=3 and hour<12:
        speak("Здравствуйте, как вам утро?")
    elif hour>=12 and hour<17:
        speak("Добрый день, сэр")
    else:
        speak("Чудный сегодня вечер не так ли?")

'''End'''



''' Related To Weather '''
def whatTheWeather():
    speak(weather())

def iChangedThePlace(newPlace):
    placeWhereIAm = newPlace

def weatherInPlace(place):
    nameOfThePlace = translateTo(place, 'en')
    speak(weatherIn(nameOfThePlace))
"""End"""




''' Telegram Functions '''
fin = open("name_username.txt", "r", encoding="UTF8")
baseNameUsername = {}
baseUsernameName = {}
for line in fin:
    ar = [i for i in line.strip().split(", ")]
    baseNameUsername[ar[0]] = ar[1]
    baseUsernameName[ar[1]] = ar[0]


def missedMessages():
    global baseUsernameName
    fin = open("Missed_Massages.txt", "r")
    youMissed = "Так так так, посмотрим что здесь. "
    for line in fin:
        array = [ i for i in line.split(", ").strip()]
    name = baseUsernameName[array[1]]
    for i in range(len(array)):
        youMissed = youMissed + array[0]+" это вам написал "+name+" в "+array[2] + " также "
    fin.close()
    #To clean the file
    fin = open("Missed_Massages.txt","w")
    fin.close()
    #
    speak(youMissed+"это всё.")

def humor():
    speak(startTheHumorFunctions())

def writeTo(name):
    global baseNameUsername
    # create my client
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(username, api_id, api_hash)
    if(name in baseNameUsername.keys()):
        username = baseNameUsername[name]
    else:
        while True:
            speak("Такого имени не найдено, повторите пожалуйста")
            name = listenTheAnswer()
            if(name in baseNameUsername):
                speak("Имя найдено, спасибо за терпение)")
                break

    with client:
        client.loop.run_until_complete(writeMessage(client, username))

    client.start()
    client.run_until_disconnected()

async def writeMessage(client, username):
    while True:
        speak("Что вы хотите написать?")
        whatToWrite = listenTheAnswer()
        await client.send_message(username, whatToWrite)
        speak("Ещё чтонебудь напишем?")
        answer = listenTheAnswer()
        if("нехочу" in answer or "не " in answer):
            speak("Хорошо")
            break

''' End '''










'''Related To the Internet services'''

whatToWatch = { "cleanTheRequest":("давай","открой","можешь","открыть","я хочу","посмотреть")}
def openYouTube():
    speak("Что вы хотите посмотреть?")
    whatToWatch = listenTheAnswer()
    for x in whatToWatch['cleanTheRequest']:
        whatToWatch = whatToWatch.replace(x, "").strip()
    if("рекоменлашки" in whatToWatch or "рекомендации" in whatToWatch or "реки" in whatToWatch or "главную" in whatToWatch or "рек" in whatToWatch):
        webbrowser.open_new_tab("https://www.youtube.com")
    else:
        browser = webdriver.Chrome()
        browser.get("https://www.youtube.com")
        first_pole = browser.find_element_by_css_selector('input[id = "search"]')
        first_pole.send_keys(f"{whatToWatch}")
        time.sleep(5)

#Search the wikipedia
def wiki(request):
    speak('Минутку')
    request = translateTo(request, 'en')
    try:
        results = wikipedia.summary(request, sentences=1)
        results = translateTo(results, 'ru')
        results = str(results)
        speak(results)
    except:
        speak("Запроса небыло найдено.")

#Translate to
def translation(request):
    if("английский" in request or "англ" in request):
        request = request.replace("на англ ", "").replace("на английский ", "")
        translat = translateTo(request, "en")
        speak(translat)
    elif("испанский" in request):
        request = request.replace("на испанский ", "")
        translat = translateTo(request, "es")
        speak(translat)
    elif ("французкий" in request):
        request = request.replace("на французский ", "")
        translat = translateTo(request, "fr")
        speak(translat)
    elif("немецкий" in request):
        request = request.replace("на немецкий ", "")
        translat = translateTo(request, "de")
        speak(translat)
    elif("португальский" in request):
        request = request.replace("на португальский ", "")
        translat = translateTo(request, "pt")
        speak(translat)

def translateTo(request, lg):
    translator = google_translator()
    translate_text = translator.translate(request, lang_tgt=lg)
    return translate_text


def openGoogle():
    browser = webdriver.Chrome()
    browser.get("https://www.google.com")
    time.sleep(5)

#Deliver something
def deliver():
    speak("Что вы хотите заказать? Давайте по одному.")
    dish = listenTheAnswer()
    browser = webdriver.Chrome()
    browser.get("https://glovoapp.com/ua/uk/kiyiv-praviy-bereg/")
    time.sleep(5)
    while(True):
        if("всё" in dish or "все" in dish):
            break
        elif("я сам" in dish or "сам" in dish):
            return
        else:
            first_pole = browser.find_element_by_css_selector("input.el-input__inner[type = 'text'] ")
            first_pole.send_keys(f"{dish}")
def searchInBrowser(request):
    browser = webdriver.Chrome()
    browser.get("https://www.google.com")
    time.sleep(5)
    first_pole = browser.find_element_by_css_selector('input[jsaction = "paste:puy29d;"]')
    first_pole.send_keys(f"{request}")

"""End"""





"""Without Theme"""
'Current Time'
def ctime():
    now = datetime.datetime.now()
    speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

'Open Program'
listOfPositions = {"второе":2,"третье":3,"четвёртое":4,"пятое":5,"шестое":6,"седьмое":7,"восьмое":8}
def openProgram(request):
    request = translateTo(request, "en")
    pg.click(354, 1056)
    pg.PAUSE=5
    lenOfRequest = len(request)
    while lenOfRequest>3:
        pg.typewrite(f"{request[:lenOfRequest]}")
        pg.PAUSE=5
        speak("Вы увидели нужную программу?")
        answer = listenTheAnswer()
        if("да" in answer):
            speak("Приложени первое в списке?")
            answer = listenTheAnswer()
            if("да" in answer):
                pg.typewrite(['Enter'])
                pg.PAUSE=5
            else:
                speak("Если не знаете или не можете его правильно открыть скажите да")
                answer = listenTheAnswer()
                if("да" in answer):
                    speak("Какое оно в списке позиций?")
                    answer = listenTheAnswer()
                    try:
                        position = listOfPositions[answer]
                        for i in range(1, position):
                            pg.typewrite(["down"])
                            pg.PAUSE=5
                        pg.typewrite(["Enter"])
                        break
                    except:
                        speak("Простите но всё сложнее чем мы думали, наведите курсор на приложение и два раза быстро нажмите левую кнопку мыши")
        lenOfRequest-=1


"""Write down the ideas"""
def writeDown(request):
    fin = open("CreatedIdeas.txt", "a")
    fin.write(request + '\n')
    fin.close()
def readTheIdeas():
    fin.open("CreatedIdeas.txt", "r")
    speak("Вы просили записать")
    for line in fin:
        idea = line.strip()
        speak(idea)
        speak("Также")
    speak("Это всё.")
    fin.close()

"""What to buy in the market"""
def whatToBuy(request):
    fin = open("MarketList.txt", "a")
    fin.write(request+'\n')
    fin.close()
def neededProducts():
    fin = open("MarketList.txt","r")
    speak("Вам нужно купить")
    for line in fin:
        speak(line.strip('\n'))
    speak("Это всё")
def cleanTheMarketList():
    fin = open("MarketList.txt", "w")
    fin.close()

"""End"""






'''Related To Pills'''
def remindPills():
    speak(remind())

def addNewPills():
    speak("Какие таблетки мы добавим?")
    pill = listenTheAnswer()
    speak("Сколько раз в день принимаем?")
    howManyTimes = listenTheAnswer()
    speak("Есть ли особые рекомендации?")
    specificRecommendations = listenTheAnswer()

    if("нет" in specificRecommendations or "никаких" in specificRecommendations):
        specificRecommendations="none"
    elif("перед едой" in specificRecommendations or "перед" in specificRecommendations):
        specificRecommendations = "before food"
    elif("после еды" in specificRecommendations or "после" in specificRecommendations):
        specificRecommendations = "after food"

    array = [pill, howManyTimes, specificRecommendations]

    speak(addPills(array))


def deleteSomePells(name):
    name = translateTo(name, 'en')
    if(deletePill(name)):
        speak("Сделанно, сэр")
    else:
        speak("К сожалению этих таблеток нет в списке")

def iAmGoingToEat():
    speak(iAmEating())
    
'''End'''




"""Pick up clothes"""

def forStreet():
    global placeWhereIAm
    weather = weatherPl(placeWhereIAm)
    suteableClothes = goToStreet(weather)

    whatToDress = "Я предлагаю вам одеть "
    for i in suteableClothes.keys():
        if(len(suteableClothes[i])>1):
            whatToDress += suteableClothes[i][0]+" или "+suteableClothes[i][1] + " Также "
        else:
            whatToDress += suteableClothes[i][0] + " и "
    whatToDress += "Как вам такой вариант?"
    speak(whatToDress)

def forSport(where):
    global placeWhereIAm
    if("на улице" in where and "на улицу" in where):
        weatherNow = weatherPl(placeWhereIAm)
        suteableClothes = goToSport(weatherNow, "opened")

    else:
        weatherNow = weatherPl(placeWhereIAm)
        suteableClothes = goToSport(weatherNow, "closed")

    whatToDress = "Я предлагаю вам одеть "
    for i in suteableClothes.keys():
        if (len(suteableClothes[i]) > 1):
            whatToDress += suteableClothes[i][0] + " или " + suteableClothes[i][1] + " Также "
        else:
            whatToDress += suteableClothes[i][0] + " и "
    whatToDress += "Как вам такой вариант?"
    speak(whatToDress)

def clotheNotAviable(clothe):
    try:
        nowIsNotAvailable(clothe)
        speak("Сделанно")
    except:
        speak("Этой вещи нет в списке")

def clotheAvailable(clothe):
    try:
        nowIsAvailable(clothe)
        speak("Выполненно")
    except:
        speak("Этой вещи нет в списке")

































'''Let`s start the program '''

lastCall = time.clock()

os.system(r"J2_Telegram_Modulo.py") # To start Telegram Modulo

with m as source:
    r.adjust_for_ambient_noise(source)


stop_listening = r.listen_in_background(m, callbackForCommands)
while True: time.sleep(0.1) # infinity loop
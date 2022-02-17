import configparser
import asyncio
from telethon.sync import TelegramClient
from telethon import connection
import pyttsx3


from telethon.tl.functions.messages import GetHistoryRequest


async def find_humor(channel, client):
	startMsg = 0    # номер записи, с которой начинается считывание
	limitMsg = 5   # максимальное число записей, передаваемых за один раз
	noMoreMessages = 0  # поменяйте это значение, если вам нужны не все сообщения

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=startMsg,
			offset_date=None, add_offset=0,
			limit=limitMsg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			if ("@anekdoti69" in message.to_dict()['message'] and len(message.to_dict()['message'])>40):
				return message.to_dict()['message']
				break
		startMsg += 1


async def main(client, speak_engine):
	url = "https://t.me/anekdoti69"
	channel = await client.get_entity(url)
	#await find_participants(channel)
	speak(await find_humor(channel, client), speak_engine)

def startTheHumorFunctions():
	#voice
	speak_engine = pyttsx3.init("sapi5")
	voices = speak_engine.getProperty('voices')
	speak_engine.setProperty('voice', voices[0].id)

	config = configparser.ConfigParser()
	config.read("config.ini")

	api_id = config['Telegram']['api_id']
	api_hash = config['Telegram']['api_hash']
	username = config['Telegram']['username']

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	client = TelegramClient(username, api_id, api_hash)

	with client:
		client.loop.run_until_complete(main(client, speak_engine))

	client.start()
	client.run_until_disconnected()

def speak(what, speak_engine):
    speak_engine.say(what)
    speak_engine.runAndWait()
    lastCall = time.clock()

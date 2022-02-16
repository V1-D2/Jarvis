import configparser

from telethon.sync import TelegramClient
from telethon import connection

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
			print(message)
			if ("@anekdoti69" in message.to_dict()['message'] and len(message.to_dict()['message'])>40):
				return message.to_dict()['message']
				break
		startMsg += 1


async def main(client):
	url = "https://t.me/anekdoti69"
	channel = await client.get_entity(url)
	#await find_participants(channel)
	print(await find_humor(channel, client))

def startTheHumorFunctions():
	config = configparser.ConfigParser()
	config.read("config.ini")

	api_id = config['Telegram']['api_id']
	api_hash = config['Telegram']['api_hash']
	username = config['Telegram']['username']

	client = TelegramClient(username, api_id, api_hash)

	with client:
		client.loop.run_until_complete(main(client))

	client.start()
	client.run_until_disconnected()

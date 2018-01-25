import atexit
import configparser
import telegram
import time

from binance.client import Client
from datetime import datetime

#Bot and config instances
config = None
telegram_bot = None
binance_bot = None
#general variables
refresh_rate = -1
chat_id = -1
time_started = -1
orders = []

def start():
	init()
	process()

def init():
	#Print starting string, and save the current time
	print("Starting your bot...\n")
	global time_started
	time_started = str(datetime.now())
	#Initialize the config parser and bots
	initConfig()
	initTelegram()
	initBinance()
	#Print and send success messages
	print("\nBot started successfully... Beginning processing...\n")
	telegram_bot.send_message(chat_id=chat_id, text=("Your bot instance (Started at " + time_started + ") has started. Monitoring has started."))

def initConfig():
	#Initialize the config file
	global config
	config = configparser.ConfigParser()
	config.read("config.ini")
	#Raise an error if it cannot import the configuration datasets
	if('GENERAL' in config):
		global refresh_rate
		refresh_rate = config['GENERAL']['refresh_rate']
	else:
		raise ValueError("Cannot find the 'General' dataset in your config file.")

def initTelegram():
	#Telegram
	if('TELEGRAM' in config):
		#Initialize the Telegram bot
		global telegram_bot, chat_id
		telegram_bot = telegram.Bot(token=config['TELEGRAM']['token'])
		chat_id = config['TELEGRAM']['chat_id']
		#Fetches and prints bot ID to ensure valid token
		try:
			print("Your Telegram API information is valid (Bot ID: {})!".format(telegram_bot.get_me().id))
		except: 
			print("Your Telegram API information is invalid.")
	else:
		raise ValueError("Cannot find the 'Telegram' dataset in your config file.")

def initBinance():
	#Binance
	if('BINANCE' in config):
		#Initialize the Binance bot
		global binance_bot
		binance_bot = Client(config['BINANCE']['key'], config['BINANCE']['secret'])
		#Fetches your BTC address to test successful API information
		btc_address = binance_bot.get_deposit_address(asset='BTC')
		if(btc_address.get("success") == True):
			print("Your Binance API information is valid!")
		else:
			print("Your Binance API information is invalid.")
	else:
		raise ValueError("Cannot find the 'Binance' dataset in your config file.")

def process():
	global orders
	while(1):
		#Fetches all open orders
		open_orders = parseOrders()
		#Sleep for refresh_rate amount of seconds
		time.sleep((int(refresh_rate)*60))

def parseOrders():
	#Fetch open orders from Binance and create an empty list to hold the parsed orders
	open_orders = binance_bot.get_open_orders()
	parsed = []
	for order in open_orders:
		#Append a new item to the parsed list that stores the symbol and orderID delimited by a bar '|'
		item = order.get("symbol") + "|" + order.get("clientOrderId")
		parsed.append(item)
	return parsed

def addOrder(order):
	pass

def removeOrder(order):
	pass

@atexit.register
def exit():
	#Send an "exiting bot" message before exiting script
	telegram_bot.send_message(chat_id=chat_id, text=("Your bot instance (Started at " + time_started + ") has stopped. Monitoring has exited."))
	print("Bot has exited successfully...")

if(__name__ == "__main__"):
	start()
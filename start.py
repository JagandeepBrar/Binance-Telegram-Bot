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

#General variables
refresh_rate = -1
chat_id = -1
time_started = -1

#Order-related variables
orders = []
send_open = False
send_closed = False

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
	telegram_bot.send_message(chat_id=chat_id, text=("Your bot instance (" + time_started + ") has started. Monitoring has begun."))

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
	while(1):
		#Fetches all open orders
		open_orders = binance_bot.get_open_orders()
		#Iterate through all orders fetched from Binance and append any new orders
		for order in open_orders:
			if not order in orders:
				addOrder(order)
		#Iterate through all orders in our own list and remove any orders not on Binance anymore
		for order in orders:
			if not order in open_orders:
				closeOrder(order)
		#Sleep for refresh_rate amount of seconds
		time.sleep((int(refresh_rate)*60))

def addOrder(order):
	#Add the order to the global list
	global orders
	orders.append(order)
	#Send a message to Telegram if enabled in the config
	if(config['GENERAL'].getboolean('update_open')):
		msg = "*{} Order Created*\n\n*Symbol*: {}\n*Price*: {}\n*Quantity*: {}".format(order.get("side").capitalize(), order.get("symbol"), order.get("price"), order.get("origQty"))
		telegram_bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

def closeOrder(order):
	#Remove the order from the global list
	global orders
	orders.remove(order)
	#Send a message to Telegram if enabled in the config
	if(config['GENERAL'].getboolean('update_closed')):
		msg = "*{} Order Closed*\n\n*Symbol*: {}\n*Price*: {}\n*Quantity*: {}".format(order.get("side").capitalize(), order.get("symbol"), order.get("price"), order.get("origQty"))
		telegram_bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)


@atexit.register
def exit():
	#Send an "exiting bot" message before exiting script
	telegram_bot.send_message(chat_id=chat_id, text=("Your bot instance (" + time_started + ") has exited. Monitoring has stopped."))
	print("Bot has exited successfully...")

if(__name__ == "__main__"):
	start()
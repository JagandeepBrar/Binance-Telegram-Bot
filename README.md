# Binance-Telegram-Script
A basic Telegram bot (script) that sends updates if a transaction has gone through on Binance. 
Written for Python 3.6.4.

# Usage

- Copy `config.ini.sample` to `config.ini` and fill all of the data
- `pip install -r requirements`
- `python start.py`

For a deeper installation guide (including creating a Telegram bot): https://www.jagandeepbrar.io/binance-telegram-bot-guide/

# Config

- GENERAL
	- `refresh-rate`: (int) The number of minutes to wait before refreshing orders from Binance (Default: 1)
	- `update-open`: (yes/no) A boolean on if to send Telegram messages for new open buy/sell orders (Default: yes)
	- `update-closed`: (yes/no) A boolean on if to send Telegram messages for closed buy/sell orders (Default: yes) 
- BINANCE
	- `key`: (string) API key fetched from Binance's website
	- `secret`: (string) API secret fetched from Binance's website
- TELEGRAM
	- `token` (string) Bot token fetched from @Botfather on Telegram
	- `chat_id` (string) Your chat ID on the chat to send these messages
		- *Get your personal/group chat ID easily from this bot: https://telegram.me/myidbot*

# Notes

- If enabled, a message will be sent even if you closed the buy/sell order yourself
- A notification will not be sent if a buy/sell order is created and completed both before the script has refreshed
	
# APIs Used

- [Python-Binance](https://github.com/sammchardy/python-binance)
- [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot)

# Donation

No donation or anything is needed at all, but if you found the bot useful, I'll shamelessly leave a few of my addresses below:
- **BTC**: 3JcxCYrVtQpRWfnocjn544RC6qpt1MDsAq
- **BCH**: 1CRroNdidp4oGfiBpb63H7Feq8ou4TJY8M
- **ETH**: 0x6bdddb6f91cbdc5198bc9fed6f1f8f5686fd3a7e

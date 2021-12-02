import asyncio
import json
import os
import sys

import aiohttp
import telegram
from telegram.ext import Updater
from telegram import Update
from utils import create_telegram_msg

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

updater = Updater(token=config["telegram_token"], use_context=True)
bot = updater.bot
job_queue = updater.job_queue

#https://t.me/crypto_signals247_bot
# def send():
#     bot.send_message(text="Hello!")

bot.send_message(chat_id=-730453456, text="Hello!")

# async def signals():
#     url = config['signals_api_endpoint']
#     async with aiohttp.ClientSession() as session:
#         raw_response = await session.get(url)
#         response = await raw_response.text()
#         response = json.loads(response)
#         print(response)
#     if response['signals']:
#         if response['count'] == 1:
#             print("count = 1")
#             print(response)
#             bot.send_message(text=create_telegram_msg(response['signals'][0]), parse_mode=telegram.ParseMode.MARKDOWN_V2) #chat_id="123",
#             await asyncio.sleep(30)
#         else:
#             for i in response['signals']:
#                 # send telegram msg here
#                 bot.send_message(text=create_telegram_msg(response['signals'][0]), parse_mode=telegram.ParseMode.MARKDOWN_V2)
#             await asyncio.sleep(30)

# job_queue.run_repeating(send, 10)     #, context=twitter
updater.start_polling()
# updater.idle()

import asyncio
import json
import os
import platform
import sys

import aiohttp
import telegram
from discord.ext import tasks
from discord.ext.commands import Bot
from discord.utils import get
from telegram.ext import Updater

from utils import *

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()
discord_bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
coin = CoinGeckoAPI()

updater = Updater(token=config["telegram_token"], use_context=True)
telegram_bot = updater.bot


@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    if not signals.is_running():
        signals.start()
    updater.start_polling()     #timeout=30


@tasks.loop(minutes=1)
async def signals():
    url = f"https://api.cryptoqualitysignals.com/v1/getSignal/?api_key=FREE&interval=1"

    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

    channels = []
    for id in config['discord_channel_ids']:
        channels.append(get(discord_bot.get_all_channels(), id=id))
    print(response)
    if response['signals']:
        if (response['signals'][0]['currency']).lower() == "usdt":
            if response['count'] == 1:
                print("count = 1")
                embed = signals_helper(response['signals'][0])
                print(response)
                try:
                    telegram_bot.send_message(chat_id=config['telegram_channel_id'], text=create_telegram_msg(response['signals'][0]),
                                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
                except Exception:
                    print(Exception)
                for channel in channels:
                    await channel.send(embed=embed)
                await asyncio.sleep(30)
            else:
                for i in response['signals']:
                    embed = signals_helper(i)
                    try:
                        telegram_bot.send_message(chat_id=config['telegram_channel_id'],
                                                  text=create_telegram_msg(response['signals'][0]),
                                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    except Exception:
                        print(Exception)
                    for channel in channels:
                        await channel.send(embed=embed)
                await asyncio.sleep(30)


discord_bot.run(config["discord_token"])

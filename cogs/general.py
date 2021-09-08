import json
import os
import sys
import time
from datetime import datetime
import aiohttp
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_volume(currency):
        key = 'c9107b23-aa25-4d10-8948-ff6e3c2c6739'
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            data = data['data']
            for dict in data:
                if dict['symbol'] == currency:
                    return dict['quote']['USD']['volume_24h']

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    @staticmethod
    def convertTimeStamp(time):
        months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
                  11: "Nov", 12: "Dec"}
        time = time.rstrip().split()
        date = time[0].split("-")
        time = datetime.strptime(time[1], "%H:%M:%S")
        month = months[int(date[1])]
        return f"{month} {date[2]}, {time.strftime('%I:%M %p')}"

    @staticmethod
    def signals_helper(signal):
        embed = discord.Embed(
            title="Quality Signals Channel",
            description="",
            color=0xD5059D
        )
        embed.add_field(
            name=f"{general.convertTimeStamp(signal['timestamp'])}",
            value=chr(173),
            inline=False
        )
        embed.add_field(
            name=f"💎 Buy #{signal['coin']}/#{signal['currency']}",
            value=chr(173),
            inline=False
        )

        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(
            name=f"🛒 Entry Zone: {signal['buy_start']}-{signal['buy_end']}",
            value=chr(173),
            inline=False
        )
        embed.add_field(
            name=f"💵 Current ask: {signal['ask']}",
            value=chr(173),
            inline=False
        )
        embed.add_field(
            name=f"🎯 Target 1: {signal['target1']} ({((float(signal['buy_end']) - float(signal['target1'])) / float(signal['buy_end']) * 100)}%)",
            value=chr(173),
            inline=False
        )
        if 'target2' in signal:
            embed.add_field(
                name=f"🎯 Target 2: {signal['target2']} ({((float(signal['buy_end']) - float(signal['target2'])) / float(signal['buy_end']) * 100)}%)",
                value=chr(173),
                inline=False
            )
        if 'target3' in signal:
            embed.add_field(
                name=f"🎯 Target 3: {signal['target3']} ({((float(signal['buy_end']) - float(signal['target3'])) / float(signal['buy_end']) * 100)}%)",
                value=chr(173),
                inline=False
            )

        embed.add_field(name=chr(173), value=chr(173))

        if 'stop_loss' in signal:
            embed.add_field(
                name=f"🚫 Stop loss: {signal['stop_loss']} ({((float(signal['stop_loss']) - float(signal['buy_end'])) / float(signal['buy_end'])) * 100}%)",
                value=chr(173),
                inline=False
            )

        embed.add_field(
            name=f"💰 Volume #{signal['currency']}: {general.get_volume(signal['currency'])}",
            value=chr(173),
            inline=False
        )

        embed.add_field(
            name=f"💰 Volume #{signal['coin']}: {general.get_volume(signal['coin'])}",
            value=chr(173),
            inline=False
        )

        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(
            name=f"⏳ {signal['type']}",
            value=chr(173),
            inline=False
        )

        if "risk_level" in signal:
            if int(signal['risk_level']) <= 2:
                embed.add_field(
                    name=f"⚠ Risk: {signal['risk_level']}/5 LOW",
                    value=chr(173),
                    inline=False
                )
            elif int(signal['risk_level']) == 3:
                embed.add_field(
                    name=f"⚠ Risk: 3/5 MEDIUM",
                    value=chr(173),
                    inline=False
                )
            elif int(signal['risk_level']) == 4:
                embed.add_field(
                    name=f"⚠ Risk: 4/5 MEDIUM HIGH",
                    value=chr(173),
                    inline=False
                )
            elif int(signal['risk_level']) == 5:
                embed.add_field(
                    name=f"⚠ Risk: 5/5 HIGH",
                    value=chr(173),
                    inline=False
                )
        return embed

    @commands.command(name="cqs", description="Crypto Signals")
    async def crypto_quality_signals(self, context):
        url = f"https://api.cryptoqualitysignals.com/v1/getSignal/?api_key=FREE&interval=3"
        async with aiohttp.ClientSession() as session:
            while True:
                raw_response = await session.get(url)
                response = await raw_response.text()
                response = json.loads(response)
                webhook = Webhook.from_url(
                    "https://discord.com/api/webhooks/885086293002965012/M-y_kPF19bcEhfql0HaXfRhvaQdBEMFKLUKp3nztaR5ufRD_EhPnGJOAIBwtV8TW1YJd",
                    adapter=RequestsWebhookAdapter())

                print(response)
                if response['signals']:
                    if response['count'] == 1:
                        embed = self.signals_helper(response['signals'][0])
                        user = discord.utils.get(context.guild.members, name="TheBlackestMamba", discriminator=3158)
                        await webhook.send(content=f"{user.mention}", embed=embed)
                    else:
                        for i in range(response['count']):
                            embed = self.signals_helper(response['signals'][i])
                            user = discord.utils.get(context.guild.members, name="TheBlackestMamba", discriminator=3158)
                            await webhook.send(content=f"{user.mention}", embed=embed)
                time.sleep(30)


def setup(bot):
    bot.add_cog(general(bot))

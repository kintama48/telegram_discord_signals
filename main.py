from bot import *
from telegram_bot import *
import json

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# discord_bot.run(config["discord_token"])
# updater.start_polling()
#updater.idle()
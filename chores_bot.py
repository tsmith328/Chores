# Posts a message to GroupMe using the website's REST API

# Written by: Tyler Smith
# tsmith328@gatech.edu
# February 2017

import json
import requests

# POST URL
api = ""

# Bot id
bot_id = ""

# Bot config file
BOT_CONFIG = 'config/bot.cfg'

# Initialize the bot and post the chore assignments found in chores to GroupMe
def postChores(chores):
    init()
    payload = {}
    payload['bot_id'] = bot_id
    payload['text'] = '\n'.join(["%s: %s" % (k,v) for k,v in chores.items()])
    requests.post(api, json=payload)

# Initialize using configuration file found at BOT_CONFIG
def _init():
    global api
    global bot_id
    f = open(BOT_CONFIG, 'r')
    try:
        bot = json.load(f)
        bot_id = bot['bot_id']
        api = bot['api_url']
        f.close()
    except:
        print("Incorrect bot.cfg")
        f.close()
        exit()
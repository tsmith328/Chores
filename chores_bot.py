#! usr/bin/env python

import json
import requests

# POST URL
api = ""

# Bot id
bot_id = ""

# Bot config file
BOT_CONFIG = 'config/bot.cfg'

def postChores(chores):
    init()
    payload = {}
    payload['bot_id'] = bot_id
    payload['text'] = '\n'.join(["%s: %s" % (k,v) for k,v in chores.items()])
    requests.post(api, json=payload)

def init():
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
import json
import time
import requests
import random

with open('config.json') as f:
    config = json.load(f)

WEBHOOK = config['notifications']['discord']['webhook_url']
DELAY = config['check_interval_minutes'] * 60

def send_discord(msg):
    try:
        requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    except:
        pass

def check_vinted(url, last_id):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone)'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        items = r.json().get('items', [])
        new = [i for i in items if i['id'] > last_id]
        return (new[0]['id'] if new else last_id), new
    except:
        return last_id, []

last_ids = {s['url']: 0 for s in config['searches']}
send_discord("🚀 Bot Timberland DÉMARRÉ (43-47)")

while True:
    for s in config['searches']:
        last_id, new = check_vinted(s['url'], last_ids[s['url']])
        if new:
            last_ids[s['url']] = last_id
            for item in new[-3:]:
                msg = f"**{s['name']}**\n\n{item['title']}\n💶 {item['price']}€\n🔗 https://www.vinted.fr/items/{item['id']}"
                send_discord(msg)
                time.sleep(1)
    time.sleep(DELAY * (1 + random.randint(-20,20)/100))
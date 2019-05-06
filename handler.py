import asyncio
import aiohttp
import base64
import json
import os
import schedule
import time


webhook_url = os.getenv('SLACK_WEBHOOK_URL')
payload = {'text': 'hello'}

basic_auth = f"{os.getenv('BASIC_AUTH_NAME')}:{os.getenv('BASIC_AUTH_PASS')}"
encode=base64.b64encode(basic_auth.encode('utf-8'))
headers = {"Authorization": f"Basic {encode.decode('utf-8')}"}


def check_health_every_secound(event, context):
    schedule.every().second.do(check_health)

    while True:
        schedule.run_pending()
        time.sleep(1)

def check_health():
    url_list = os.getenv('URL_LIST').split(',')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([asyncHttpGet(url) for url in url_list]))

async def asyncHttpGet(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if not 200 <= resp.status < 400:
                session.post(webhook_url, data=json.dumps(payload))

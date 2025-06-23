

import pprint
import json
from discord_webhook import DiscordWebhook,DiscordEmbed
from time import sleep
import shutil
with open('config.json') as config_file:
    config = json.load(config_file)

try:
    url = config['discord']['url']
    api_id = config['telegram']['api_id']
    api_hash = config['telegram']['api_hash']
    phone = config['telegram']['phone']
    channel_ids = config['telegram']['channel_ids']
    wait = config['telegram']['wait']
except:
    print('Error processing config file')

print(url)
from telethon import TelegramClient
last_messages = dict()
client = TelegramClient('session', api_id, api_hash)
async def main():
    while(True):
        print("Beginning check")
        async for dialog in client.iter_dialogs():
            if(dialog.id in channel_ids):
                print(dialog.name, 'has ID', dialog.id)
                if dialog.id in last_messages.keys():
                    if last_messages[dialog.id] != dialog.message.text:
                        print("Forwarding new message from:",dialog.id)
                        await send_webhook(dialog.message,dialog)
                        last_messages[dialog.id] = dialog.message
                else:
                    print("Forwarding new message from:",dialog.id)
                    print(dialog.message.id)
                    await send_webhook(dialog.message,dialog)
                    last_messages[dialog.id] = dialog.message.text
        sleep(wait)
        print("Cleaning previous download folder...")
        shutil.rmtree("./downloads/",ignore_errors=True)

                
async def send_webhook(message,dialog):
    hook = DiscordWebhook(url=url)
    embed = DiscordEmbed(
        title=dialog.name,description=message.text
    )
    if message.forward:
        embed.add_embed_field("Forwarded:","True")
    embed.set_timestamp()
    hook.add_embed(embed)
    hook.execute()
    print("Sending message content for",dialog.name)
    if message.media is not None:
        print("Media attachement detected,cleaning hook")
        hook = DiscordWebhook(url=url)
        print("Downloading attachement")
        res = await client.download_media(message,file="./downloads/")
        filestream = open(res,"rb")
        hook.add_file(filestream,filename=res)
        print("Forwarding attachement")
        hook.execute()
with client:
    client.loop.run_until_complete(main())
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import asyncio
import discord
import os
import threading
import json, time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

messageQueue = []
acceptedEnds = ['.png', '.gif', '.jpg']
watchlist = {}

bot = commands.Bot(command_prefix=';')


def listening():
    listener = Listener(('', 4000))
    while True:
        try:
            conn = listener.accept()
            msg = conn.recv()  # I just assume we'll always be receiving json, and will code accordingly
            messageQueue.append(msg)
        except Exception as e:
            print(e)
        time.sleep(0.1)


@bot.event
async def on_ready():
    thr = threading.Thread(target=listening)
    thr.start()
    while True:  # we always sit on a loop, waiting for the message queue to have something in it, then process accordingly
        try:
            if len(messageQueue) > 0:
                jsonPack = messageQueue.pop(0)
                print(jsonPack)
                channel = bot.get_channel(jsonPack['channel'])
                if jsonPack['response_id'] is None:
                    if type(jsonPack['output']) is str:
                        if os.path.isfile(jsonPack['output']):
                            if jsonPack['output'][-4:] in acceptedEnds:  # every file we try to upload has to end with one of the 3 above endings, for safety
                                try:  # just in case for some reason something ends with that but isn't a valid filename...
                                    sent_message = await channel.send(file=discord.File(jsonPack['output']))
                                    url = sent_message.attachments[0].url
                                    sent_message2 = await channel.send(url)
                                    await asyncio.sleep(0.1)
                                    await sent_message.delete()
                                    watchlist[jsonPack['message_id']] = sent_message2.id
                                    print(watchlist)
                                except Exception as e:
                                    await channel.send(str(e))
                                if jsonPack['output'][0:5].isdigit():
                                    os.remove(jsonPack['output'])
                            else:
                                await channel.send('idk what you did, but I can\'t let you have that :\'(')
                        else:
                            await channel.send(jsonPack['output'])
                    else:
                        await channel.send(str(jsonPack['output']))
                else:  # this is just mirrored logic because I'm too lazy to find a way to make it not so for now...
                    message = await channel.fetch_message(jsonPack['response_id'])
                    if type(jsonPack['output']) is str:
                        if os.path.isfile(jsonPack['output']):
                            if jsonPack['output'][-4:] in acceptedEnds:  # every file we try to upload has to end with one of the 3 above endings, for safety
                                try:  # just in case for some reason something ends with that but isn't a valid filename...
                                    sent_message = await channel.send(file=discord.File(jsonPack['output']))
                                    url = sent_message.attachments[0].url
                                    await message.edit(content=url)
                                    await asyncio.sleep(0.1)
                                    await sent_message.delete()
                                except Exception as e:
                                    await message.edit(content=str(e))
                                if jsonPack['output'][0:5].isdigit():
                                    os.remove(jsonPack['output'])
                            else:
                                await message.edit(content='idk what you did, but I can\'t let you have that :\'(')
                        else:
                            await message.edit(content=jsonPack['output'])
                    else:
                        await message.edit(str(content=jsonPack['output']))
            await asyncio.sleep(0.05)
        except Exception as e:
            print(e)
    # await mother(('', 5000))

@bot.event
async def on_raw_message_edit(payload):
    print('it happened?')
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    print('content:', message.content)
    if payload.message_id in watchlist:
        print(watchlist[payload.message_id])
        emessage = await channel.fetch_message(watchlist[payload.message_id])
        try:
            c = Client(('localhost', 4001))
            out = str(message.content)[4:]
            payload = json.dumps({"channel": payload.channel_id, "message_id": payload.message_id, "userinput": out, "response_id": watchlist[payload.message_id]})
            c.send(payload)
        except Exception as e:
            await channel.send(str(e))
            print(e)


bot.run(TOKEN)
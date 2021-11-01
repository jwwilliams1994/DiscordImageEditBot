import os
import random
import datetime
import json
from multiprocessing.connection import Client
import discord  # discord.py needs replacing sometime as the author is no longer updating the library
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv
# from mcstatus import MinecraftServer
from image_mods.drawCalendar import make_calendar, add_event, get_events, remove_events, get_week
from image_mods.richardFacts import add_fact, get_facts, remove_fact
commandList = []

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')


@bot.command(name='img')
async def commanding(ctx, *, message):
    pass
    try:
        c = Client(('localhost', 4001))
        payload = json.dumps({"channel": ctx.channel.id, "message_id": ctx.message.id, "userinput": message, "response_id": None})  # pass on the command plus the contents
        c.send(payload)
    except Exception as e:
        await ctx.channel.send(str(e))
        print(e)


@bot.command(name='get_palettes')
async def get_palettes(ctx):
    p_arr = []
    for file in os.listdir():
        if file[-12:] == "_palette.png":
            p_arr.append(file[:-12])
    outstring = ', '.join(p_arr)
    await ctx.channel.send("The following palettes are available:")
    await ctx.channel.send(outstring)


@bot.command(name='read')
async def readthis(ctx, arg):
    try:
        print(arg)
        test = arg.encode('unicode_escape')
        print(str(test)[2:-1], arg)
        if str(test)[2:-1] == str(arg):
            print("true")
        print(test)
    except:
        print("failed...")


@bot.command(name='conch')
async def magicConch(ctx):
    conchAnswers = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
                    'Don\'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
                    'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.',
                    'Yes - definitely.', 'You may rely on it.']
    answer = random.randint(0, 19)
    client = Client(('localhost', 4000))
    response = ":shell:" + conchAnswers[answer]
    payload = {"channel": ctx.channel.id, "message_id": ctx.message.id, "userinput": None, "response_id": None, "output": response}
    client.send(payload)

# @bot.command(name='temp')
# async def magicConch(context):
#     client = Client(('192.168.50.46', 5002))
#     response = "idk"
#     # payload = [context.message.channel.id, response]  # payload is [0] == channel id, [1] == message/filename
#     payload = json.dumps({"channel": ctx.channel.id, "message_id": ctx.message.id, "userinput": message, "response_id": None})
#     client.send(payload)

@bot.command(name='time')
async def givetime(ctx):
    d = datetime.datetime.now(datetime.timezone.utc)
    print(d.hour, d.minute, d.second)
    hours = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]
    minutesten = ["O\'", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    minutesone = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    minutesteen = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    if d.hour > 12 + 4:
        first = hours[d.hour - 12 - 5]
    else:
        first = hours[d.hour - 5]
    if d.minute < 11 or d.minute > 19:
        if d.minute >= 10:
            if str(d.minute)[1] != "0":
                second = minutesten[int(str(d.minute)[0])] + "-" + minutesone[int(str(d.minute)[1])]
            else:
                second = minutesten[int(str(d.minute)[0])]
        else:
            second = "O\'" + minutesone[d.minute]
    else:
        second = minutesteen[d.minute - 10]
    if d.second < 11 or d.second > 19:
        if d.second >= 10:
            if str(d.second)[1] != "0":
                third = minutesten[int(str(d.second)[0])] + "-" + minutesone[int(str(d.second)[1])]
            else:
                third = minutesten[int(str(d.second)[0])]
        else:
            third = minutesone[d.second]
    else:
        third = minutesteen[d.second - 10]
    string = "The time is: " + first + " " + second + " and " + third + " seconds."
    await ctx.channel.send(string)


@bot.command(name='calendar')
async def calendar_page(context, min: int = 0, max: int = 360, tile: int = 100):
    returned = make_calendar(min, max, tile)
    await context.channel.send(file=discord.File(returned))
    os.remove(returned)


@bot.command(name='week')
async def calendar_week(context, min: int = 0, max: int = 360, tile: int = 100):
    returned = get_week(min, max, tile)
    await context.channel.send(file=discord.File(returned))
    os.remove(returned)


@bot.command(name='add_event')
async def event_add(context, year: int, month: int, day: int, *args):
    string = ' '.join(args)
    returned = add_event(string, year, month, day)
    await context.channel.send(returned)


@bot.command(name='get_events')
async def get_event(context, year: int, month: int, day: int):
    returned = get_events(year, month, day)
    await context.channel.send(returned)


@bot.command(name='remove_event')
async def remove_event(context, year: int, month: int, day: int, index: int = 0):
    returned = remove_events(year, month, day, index)
    await context.channel.send(returned)


@bot.command(name='facts')  # facts is a json dictionary, with each name being associated to a list of user-curated 'facts'
async def get_f(context, name: str):
    returned = get_facts(name.capitalize())
    await context.channel.send(returned)


@bot.command(name='add_fact')
async def add_f(context, name: str, *args):
    string = ' '.join(args)
    returned = add_fact(name.capitalize(), string)
    emoji = bot.get_emoji(562674675981746191)
    await context.message.add_reaction(emoji)


@bot.command(name='remove_fact')
async def rem_f(context, name: str, index: int):
    returned = remove_fact(name.capitalize(), index)
    if returned == "success":
        emoji = bot.get_emoji(562674675981746191)
    else:
        emoji = bot.get_emoji(751114641048076413)
    await context.message.add_reaction(emoji)


@bot.command(name='why')
async def fortheglory(context):
    ##glory = Image.open('forthegloryofsatan.jpg')
    await context.channel.send(file=discord.File('forthegloryofsatan.jpg'))


@bot.command(name='navyseal')
async def navysealing(context):
    ##glory = Image.open('forthegloryofsatan.jpg')
    await context.channel.send(file=discord.File('navyseal.gif'))


@bot.command(name='I')
async def iguess(context, *, message):
    if message == 'guess':
        ##await context.channel.send(file=discord.File('iguess.gif'))
        await context.channel.send('https://i.imgur.com/MMaciGr.gif')


@bot.command(name='pfp')
async def getp(ctx, id):
    try:
        user = await bot.fetch_user(int(id))
        avatar = user.avatar_url
        await ctx.channel.send(avatar)
    except Exception as e:
        await ctx.channel.send(e)


# defunct as self-host is down
# @bot.command(name='God')
# async def doyouthink(context):
#     await context.channel.send('http://216.221.197.172:8081/albums/DoYouThink/DoYouThink.webm')


@bot.command(name="<:googleturtle:562674675981746191>")
async def doyouthonk(context):
    server = context.guild
    role = server.get_role(709532776940044318)
    if role is None:
        role = "Richaaaaaaard"
        await context.channel.send(role)
    else:
        await context.channel.send(role.mention)


@bot.command(name='Mr')
async def Toshi(ctx, arg):
    if arg == 'Toshi':
        role = await bot.fetch_user(459457502140956682)
        await ctx.channel.send(role.mention)

bot.remove_command('help')  # default help command with this library outputs a list of the commands, isn't particularly helpful in my case

@bot.command(name='help')
async def halp(context):
    await context.channel.send('<https://pastebin.com/cf5N0NP0>')


@bot.command(name='temp')  # queries a raspberry pi with an atmospheric sensor attached, output is a rich discord message with the data
async def temp(ctx):
    client = Client(('192.168.50.46', 5002))
    payload = {"channel": ctx.channel.id, "message_id": ctx.message.id, "userinput": "embed", "response_id": None, "output": None, "title": "3nd's Room", "url": None, "thumbnail": None}
    client.send(payload)


bot.run(TOKEN)
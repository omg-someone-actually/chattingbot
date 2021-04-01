import discord
from discord.ext import commands
from discord.ext import tasks
import random
from random import choice
from datetime import datetime
import json
from typing import MutableMapping, TypedDict

prefix = "Your prefix goes here"

#I got the list of cusswords and slurs in another file, if you want to use the prefined lists just copy paste them into this file right here.

questioned = ['?', '??', 'uh?', '???', 'hmm', 'what?', 'ok?', 'I do not understand-']

welcomers = ['hello', 'wassuh', 'wassup', 'goodmorning', 'Hey', 'hello there', 'hmm how has your day been?', 'nice to see you.', 'welcome back from the dead!', 'dont leave me again!', "hey there bud.", 'gm', ':wave:', 'hey lol', 'how has your day been?', '...']

specificwelcomes = ['hi', 'hey', 'welcome there', 'welcome', 'welcome to the server', 'enjoy your stay']

greets = ['Hello!', 'How are you?', 'Wassup everyone!', 'Heyyyyy.', 'Watcha up to?', 'Hi there :wave:', ':wave:', 'How has your day been?', 'Wassuh dude.', 'wassup', 'goodmorning', 'Hey', 'hello there', 'hmm how has your day been?', 'nice to see you.', 'welcome back from the dead!', 'dont leave me again!', "hey there bud.", 'gm', ':wave:', 'hey lol', 'how has your day been?', '...', ':|', ':)', ':(',';-;', 'hey everyone!', 'XD', 'yo what\'s up', 'yo']

funny = ['omg lol', 'LOL', 'xD', 'wow thats funny', 'lmaooo', 'lmfao xDD', 'bruh thats to funny', 'ahah', 'heh', 'xDDD', 'lool', ':rofl:', 'hmm lol', 'bruhh lmfao', 'lol', 'wtf lmfaooo', 'uh no funny has happened.']

funnies = ['omg lol', 'LOL', 'xD', 'wow thats funny', 'lmaooo', 'lmfao xDD', 'bruh thats to funny', 'ahah', 'heh', 'xDDD', 'lool', ':rofl:', 'hmm lol', 'bruhh lmfao', 'lol', 'wtf lmfaooo', 'uh no funny has happened.', 'lmao', 'lmfao', 'hehe', 'haha', 'heh', 'hah']

response = ['oh thats interesting..', 'good to hear', 'ohh ok', 'hmm lol', 'ohhh', 'thats intriging.', 'ehhh could be worse.', 'soudnds like a lot of fun-', 'hmm ok', 'that makes sense ig', 'nice to hear', 'omg ok lol', 'thats a rip ig', 'beep boop you a bot?', 'well anything is better then being a bot..', 'That seems cool actaully', 'oooof lol']

topic = ["What is your favorite movie and why?", "Would you rather be famous but poor, or rich but lonely?", "Mustang or Camaroe?", "Do you like ranch on your pizza?", "What country was you born in?", "What is your favorite video game? And what do you like most about it?", "Is a cat or a dog better?", "How has your day been? What has made it good or bad?", "Would you rather time travel 100 years in the future or 100 years in the past?", "What do you find more interesting the future of the past?", "What is a very bad TV show and why? What makes it extremely bad in your opinion?", 'Do you think reaching mars will be a big accomplishment for humanity?', 'How tall are you? Are you happy with being your height?', 'Do you have any pets? What are they?', 'What is your choice of music?', 'What are you currently doing? Anything fun?', 'Would you take 50 grand if the person you hate the most gets 100 grand?', 'Do you enjoy memes?', 'What is a funny story of something that has happened in your life?', 'What is your favorite hobbies?']

funnyreact = ['🤣', '😂', '😜', '😎', '😁', '😃', '😄', '😅', '😆', '😉', '🤐', '🥱', '🙄', '😘', '😕', '😤', '🤑', '😯', '😋']

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix= discord.ext.commands.when_mentioned_or(prefix), intents=intents)
client.remove_command('help')
client.active = True
client.activelevel = 15
client.badwords = False


@tasks.loop(seconds=1)
async def savedservers():
    save_servers()

taskstodo = [savedservers]

def activecheck(activehm):
    return random.randint(0, activehm)

@client.command()
@commands.is_owner()
async def start(ctx):
    members = 0
    for guild in client.guilds:
        members += guild.member_count
    status = f"{len(client.guilds)} servers and {members} members"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(status)))
    await ctx.send("The status is updated-")
    for task in taskstodo:
        task.start()
    await ctx.send("All tasks has started.")

@client.event
async def on_ready():
    discord.Intents.all()
    print(f"{client.user} has logged in. The bot is ready!")

@client.group(invoke_without_command=True)
async def activity(ctx):
    server = ctx.guild.id
    active_update(server)
    await ctx.send("Change my acitvity!")

@activity.command()
async def low(ctx):
    server = ctx.guild.id
    active_low(server)
    await ctx.send("I now am inactive!")

@activity.command()
async def normal(ctx):
    server = ctx.guild.id
    active_normal(server)
    await ctx.send("I am now a normal user!")

@activity.command()
async def high(ctx):
    server = ctx.guild.id
    active_high(server)
    await ctx.send("I am now super active!")


@client.group(invoke_without_command=True)
async def filter(ctx):
    await ctx.send("Turn my filter on and off!")

@filter.command()
async def on(ctx):
    server = ctx.guild.id
    filter_on(server)
    await ctx.send("The filter is now on, all cuss words will get filtered.")

@filter.command()
async def off(ctx):
    server = ctx.guild.id
    filter_off(server)
    await ctx.send("The filter is off, all cuss words are now allowed.")

@filter.command(name="low")
async def _low(ctx):
    server = ctx.guild.id
    filterlvl_low(server)
    await ctx.send("The filter is on low mode!")

@filter.command(name="medium")
async def _medium(ctx):
    server = ctx.guild.id
    filterlvl_normal(server)
    await ctx.send("The filter is on medium mode!")

@filter.command(name="high")
async def _high(ctx):
    server = ctx.guild.id
    filterlvl_high(server)
    await ctx.send("The filter is on high mode!")

class UserRecord(TypedDict):
    filterwords: int = 0
    active: int = 2
    filterlevel: int = 0

UserDatabase = MutableMapping[str, UserRecord]

def make_user_record() -> UserRecord:
    return {"filterwords": 0, "filterlevel": 0,"active": 2}

def load_users() -> UserDatabase:
    try:
        with open("servers.json") as fp:
           return defaultdict(make_user_record, json.load(fp))
    except Exception:
        return defaultdict(make_user_record)

_user_database = load_users()

def save_servers():
    with open("servers.json", "w") as fp:
        json.dump(_user_database, fp, sort_keys=True, indent=4)

def filter_on(server):
    _user_database[server]["filterwords"] = 1
    save_servers()

def filter_off(server):
    _user_database[server]["filterwords"] = 0
    save_servers()

def filter_update(server):
    _user_database[server]["filterwords"] = _user_database[server]["filterwords"]
    save_servers()

def get_filter(server) -> int:
    return _user_database[server]["filterwords"]

def active_low(server):
    _user_database[server]["active"] = 1
    save_servers()

def active_normal(server):
    _user_database[server]["active"] = 2
    save_servers()

def active_high(server):
    _user_database[server]["active"] = 3
    save_servers()

def active_update(server):
    _user_database[server]["active"] = _user_database[server]["active"]
    save_servers()

def get_active(server) -> int:
    return _user_database[server]["active"]

def filterlvl_low(server):
    _user_database[server]["filterlevel"] = 1
    save_servers()

def filterlvl_normal(server):
    _user_database[server]["filterlevel"] = 2
    save_servers()

def filterlvl_high(server):
    _user_database[server]["filterlevel"] = 3
    save_servers()

def filterlvl_update(server):
    _user_database[server]["filterlevel"] = _user_database[server]["filterlevel"]
    save_servers()

def get_filterlvl(server) -> int:
    return _user_database[server]["filterlevel"]

@client.event
async def on_message(message):
    await client.process_commands(message)
    randogreet = choice(greets)
    randofunny = choice(funny)
    randoresponse = choice(response)
    randotopic = choice(topic)
    randoreact = choice(funnyreact)
    channel = client.get_channel(794002061539934218)
    server = message.guild.id
    filtered = get_filter(server)
    filter_update(server)
    filterlvl_update(server)
    howactive = get_active(server)
    randreact = random.randint(0, 3)
    if howactive == 1:
        randactive = 20
    elif howactive == 2:
        randactive = 15
    elif howactive == 3:
        randactive = 10
    randomsend = activecheck(randactive)
    filterlevel = get_filterlvl(server)
    badwordlevel = "cuss"
    if filterlevel == 1:
        badwordlevel = nonowords
    elif filterlevel == 2:
        badwordlevel = nonowords2
    elif filterlevel == 3:
        badwordlevel == nonowords3
    if message.author.bot:
        return
    if message.author == client.user:
        return
    if message.content == "bad bot":
        await message.channel.send("Thank you for your feedback!")
        await channel.send(f"{message.author.name} says Xylos is a bad bot!")
    if message.content == "good bot":
        await message.channel.send("Thank you for your feedback!")
        await channel.send(f"{message.author.name} says Xylos is a good bot!")
    if  any(funnie in message.content for funnie in funnies):
        await message.channel.send(randofunny)
    if any(welcomer in message.content for welcomer in welcomers):
        await message.channel.send(randogreet)
        await client.wait_for('message')
        await message.channel.send(randoresponse)
    if any(specificwelcome == message.content for specificwelcome in specificwelcomes):
        await message.channel.send(randogreet)
    if randomsend == 5 and randreact == 1:
        await message.add_reaction(randoreact)
    if randomsend == 10:
        await message.channel.send(randotopic)
    if client.active == True:
        client.active = False
    if client.user.mentioned_in(message):
        await message.channel.send("ok")
    if filtered == 1 and any(nonoword in message.content for nonoword in badwordlevel):
        await message.delete()
 
    


client.run("Your bot token goes here.")

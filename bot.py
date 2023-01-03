import discord
from discord.ext import tasks
import random
import os
from player import Player
from game import Game
from dotenv import load_dotenv
import random
import datetime
from asyncio import sleep

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
client = discord.Client(intents=intents)


data = {}
raw_players = []
gametime = datetime.time(hour=0, minute=0)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        if guild.name == "The Dog Pound":
            for member in guild.members:
                for role in member.roles:
                    if role is not None and role.name == "Hockey Players":
                        player = Player(member)
                        data[member] = player
                        raw_players.append(member)
    called_once_a_day_at_7.start()
    



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$attribute"): # Change to return all atts
        updated = "Your shot is rated {0} (1-20)".format(data[message.author].atts['shot'])
        await message.channel.send(updated)

    if message.content.startswith("$reroll"): #REMOVE THIS COMMAND (or only make it available to myself to make my player better hehehe)
        data[message.author].reroll()
        updated = "Your shot is now {0}".format(data[message.author].atts['shot'])
        await message.channel.send(updated)

    if message.content.startswith('$hello'):    #REMOVE THIS COMMAND ,basic code from the API example
        test = await message.channel.send('Hello!')
        await test.edit(content=test.content+'\nBye!')
    if message.content.startswith('$shoot'):         #REMOVE THIS COMMAND, original base version of this bot, super simple 
        score = random.random()
        if score > 0.7:
            await message.channel.send('SCORED!!!')
        else:
            await message.channel.send('SAVED!!!')
    if message.content.startswith('$play') and len(raw_players) >= 12:
        players = random.sample(raw_players, 12)
        game = Game(players, data)
        await game.play(message)



@tasks.loop(time = gametime)
async def called_once_a_day_at_7():
    print("7:00pm EST")
    for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'bot-talk':
                    disc_msg = await channel.send("--DAILY GAME--")
    players = random.sample(raw_players, 12)
    game = Game(players, data)
    await game.play(disc_msg)


@called_once_a_day_at_7.before_loop
async def before_called_once_a_day_at_7():
        await client.wait_until_ready()
        print("client finished waiting")


client.run(TOKEN)

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


# stats and positions, reroll stats?
# simulated goals and stat lines
# chance of goal every 2 minutes

# shot, skating, stickhandling, passing, strength
# shot: goal odds
# skating: goal odds, breakaways?
# stickhandling: goal odds, passing, turnovers
# strength: turnovers
# passing: teammate goal odds


#write data to text file?

data = {}
raw_players = []
#gametime = datetime.time(hour=19, minute=0, second = 0) # 7pm = 19, 0, 0

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
    print("daily function called")
    



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$attribute"):
        #if message.mentions
        updated = "Your shot is rated {0} (1-20)".format(data[message.author].atts['shot'])
        await message.channel.send(updated)

    if message.content.startswith("$reroll"):
        data[message.author].reroll()
        updated = "Your shot is now {0}".format(data[message.author].atts['shot'])
        await message.channel.send(updated)

    if message.content.startswith('$hello'):
        test = await message.channel.send('Hello!')
        await test.edit(content=test.content+'\nBye!')
    if message.content.startswith('$shoot'):
        score = random.random()
        if score > 0.7:
            await message.channel.send('SCORED!!!')
        else:
            await message.channel.send('SAVED!!!')
    if message.content.startswith('$play') and len(raw_players) >= 12:
        players = random.sample(raw_players, 12)
        game = Game(players, data)
        await game.play(message)
    if message.content.startswith('$channelset'):
        disc_msg = message.channel

@tasks.loop(hours = 24)
async def called_once_a_day_at_7():
    for guild in client.guilds:
        #if guild.name == "":
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

        now = datetime.now()
        future = datetime(now.year, now.month, now.day, now.hour, now.minute+1)
        diff = (future - now).total_seconds()

        print('sleeping')
        await sleep(diff)
        print('slept')


client.run(TOKEN)

import discord
import random
import os
from player import Player
from game import Game
from dotenv import load_dotenv
import random
from time import sleep
import datetime


#intents = discord.Intents(messages=True, guilds=True, typing=True)
#intents.message_content = True
#intents.members = True
#intents.guilds = True
#intents.all()
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


client.run(TOKEN)
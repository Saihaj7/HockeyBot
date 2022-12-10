import discord
import random
import os
from dotenv import load_dotenv


intents = discord.Intents(messages=True, guilds=True, typing=True)
intents.message_content = True

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


#write data to text file


data = []
data2 = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if message.author not in data:
        data.append(message.author)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$shoot'):
        score = random.random()
        print(score)
        if score > 0.7:
            await message.channel.send('SCORED!!!')
        else:
            await message.channel.send('SAVED!!!')


client.run("OTgxNzMxNDQ5NTI0ODQ2NTky.GgGwTE.CspOyoBrN6t01-zM-iqrnC66tRsULqJ8kaeSdE")
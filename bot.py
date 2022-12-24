import discord
import random
import os
from player import Player
from game import Game
from dotenv import load_dotenv
import random
from time import sleep


#intents = discord.Intents(messages=True, guilds=True, typing=True)
#intents.message_content = True
#intents.members = True
#intents.guilds = True
#intents.all()

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

#for user in client.users:
        #print(user.name)
        #if user not in data:
            #player = Player(user)
            #data['user'] = player





# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#     async for guild in client.fetch_guilds(limit=150):
#         if guild.name == "The Dog Pound":
#             await print(guild.fetch_roles())
#             async for member in guild.fetch_members(limit=150):
#                 #print(member.status)

#                 for role in member.roles:
#                     if role is not None and role.name == "Hockey Players":
#                         player = Player(member)
#                         data[member] = player
#                         raw_players.append(member)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        if guild.name == "The Dog Pound":
            for member in guild.members:
                for role in member.roles:
                    print(role.name)
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
        #test_msg = message.channel.send('Hello!')
        #await test_msg
        #sleep(2)
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


client.run("OTgxNzMxNDQ5NTI0ODQ2NTky.GgGwTE.CspOyoBrN6t01-zM-iqrnC66tRsULqJ8kaeSdE")
import discord
import os
from dotenv import load_dotenv

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

#     async def on_message(self, message):
#         print(f'Message from {message.author}: {message.content}')

# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)
#load_dotenv()

#TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
intents = discord.Intents(messages=True, guilds=True, typing=True)
intents.message_content = True
#intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run("OTgxNzMxNDQ5NTI0ODQ2NTky.GgGwTE.CspOyoBrN6t01-zM-iqrnC66tRsULqJ8kaeSdE")
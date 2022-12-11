import discord
import random
import os
from dotenv import load_dotenv
#from time import sleep
from scipy.stats import truncnorm
from asyncio import sleep




class Game:
    def __init__(self, players):
        self.players = players
        self.score = [0, 0] # [0] = score for t1, [1] = score for t2
        if len(players) == 10:
            self.team1 = players[:5]
            self.team2 = players[5:]

    async def play(self, message):
        await message.channel.send("Team 1 vs Team 2:")
        for shot in range(30): #takes a shot a minute
            await sleep(1)
            if random.random() > 0.8:
                if random.randint(1, 2) == 1:
                    await message.channel.send("Team 1 scores!")
                    self.score[0] = self.score[0] + 1
                else:
                    await message.channel.send("Team 2 scores!")
                    self.score[1] = self.score[1] + 1
        await message.channel.send("Final Score: {0}-{1}".format(self.score[0], self.score[1]))


# xG could be first pick the distribution value, weight it by shot,
#  then take random.random() and if it lands on the range 1 - xG it is then a goal
# but what about other events like takeaways and hits? 
# maybe those should be their own random, and if number between range it will be a shot, takeaway, or a hit
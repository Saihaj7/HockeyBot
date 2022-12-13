import discord
import random
import os
from dotenv import load_dotenv
#from time import sleep
from scipy.stats import truncnorm
from asyncio import sleep

def get_truncated_normal(mean=0, sd=1, low=0, upp=20):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        
xG = get_truncated_normal(mean=0.1, sd=0.3, low=0, upp=1)
#xG.rvs()


class Game:
    def __init__(self, players, data):
        self.players = players
        self.score = [0, 0] # [0] = score for t1, [1] = score for t2
        if len(players) >= 10:
            self.team1 = players[:5]
            self.team2 = players[5:]
        self.data = data

    async def play1(self, message):
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


    async def play(self, message):
        await message.channel.send("Team 1 vs Team 2:")
        for shot in range(15): #event each minute
            #await sleep(1)
            event = random.random()
            player1 = self.data[self.team1[random.randint(0, 4)]]
            player2 = self.data[self.team2[random.randint(0, 4)]]
            if event <= 0.6: #SHOT
                if random.randint(1, 2) == 1: #Team1
                    player_xG = (player1.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        await message.channel.send("T1 Goal scored by {0}".format(player1.user.name))
                        self.score[0] = self.score[0] + 1
                else:                           #Team2
                    player_xG = (player2.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        await message.channel.send("T2 Goal scored by {0}".format(player2.user.name))
                        self.score[1] = self.score[1] + 1
            elif event <= 0.8: #HIT
                if random.randint(1, 2) == 1: #Team1
                    await message.channel.send("{0} hit {1}".format(player1.user.name, player2.user.name))
                else: #TEAM2
                    await message.channel.send("{0} hit {1}".format(player2.user.name, player1.user.name))
            elif event <= 0.9: #TAKEAWAY
                if random.randint(1, 2) == 1: #Team1
                    await message.channel.send("{0} took the puck away from {1}".format(player1.user.name, player2.user.name))
                else: #TEAM2
                    await message.channel.send("{0} took the puck away from {1}".format(player2.user.name, player1.user.name))
            else:               #BLOCK
                if random.randint(1, 2) == 1: #Team1
                    await message.channel.send("{0} blocked a shot!".format(player1.user.name))
                else: #TEAM2
                    await message.channel.send("{0} blocked a shot!".format(player2.user.name))

        await message.channel.send("Final Score: {0}-{1}".format(self.score[0], self.score[1]))


# xG could be first pick the distribution value, weight it by shot,
#  then take random.random() and if it lands on the range 1 - xG it is then a goal
# but what about other events like takeaways and hits? 
# maybe those should be their own random, and if number between range it will be a shot, takeaway, or a hit

# time of event
#missed shot messages
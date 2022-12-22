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
        
xG = get_truncated_normal(mean=0.2, sd=0.3, low=0, upp=1)
#xG.rvs()


class Game:
    def __init__(self, players, data):
        self.players = players
        self.score = [0, 0] # [0] = score for t1, [1] = score for t2
        if len(players) >= 10:
            self.team1 = players[:5]
            self.team2 = players[5:]
        self.data = data

    async def play2(self, message):
        msg = await msg.edit(content=msg.content+"\nTeam 1 vs Team 2:")
        for shot in range(30): #event every 2 "minutes"
            await sleep(1)
            if random.random() > 0.8:
                if random.randint(1, 2) == 1:
                    await msg.edit(content=msg.content+"\nTeam 1 scores!")
                    self.score[0] = self.score[0] + 1
                else:
                    await msg.edit(content=msg.content+"\nTeam 2 scores!")
                    self.score[1] = self.score[1] + 1
        await msg.edit(content=msg.content+"\nFinal Score: {0}-{1}".format(self.score[0], self.score[1]))

    async def play1(self, message):
        msg = await message.channel.send("Team 1 vs Team 2:")
        for shot in range(15): #event each minute
            await sleep(2)
            event = random.random()                                     #kys fr
            player1 = self.data[self.team1[random.randint(0, 4)]]
            player2 = self.data[self.team2[random.randint(0, 4)]]
            if event <= 0.6: #SHOT
                if random.randint(1, 2) == 1: #Team1
                    player_xG = (player1.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        await msg.edit(content=msg.content+"\nT1 Goal scored by {0}".format(player1.user.display_name))
                        self.score[0] = self.score[0] + 1
                else:                           #Team2
                    player_xG = (player2.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        await msg.edit(content=msg.content+"\nT2 Goal scored by {0}".format(player2.user.display_name))
                        self.score[1] = self.score[1] + 1
            elif event <= 0.8: #HIT
                if random.randint(1, 2) == 1: #Team1
                    await msg.edit(content=msg.content+"\n{0} hit {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    await msg.edit(content=msg.content+"\n{0} hit {1}".format(player2.user.display_name, player1.user.display_name))
            elif event <= 0.9: #TAKEAWAY
                if random.randint(1, 2) == 1: #Team1
                    await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player2.user.display_name, player1.user.display_name))
            else:               #BLOCK
                if random.randint(1, 2) == 1: #Team1
                    await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player1.user.display_name))
                else: #TEAM2
                    await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player2.user.display_name))

        await msg.edit(content=msg.content+"\nFinal Score: {0}-{1}".format(self.score[0], self.score[1]))


    async def play(self, message):
        msg = await message.channel.send("Team 1 vs Team 2:")
        for shot in range(15): #event each minute
            await sleep(2)
            event = random.random()                                     #kys fr
            player1 = self.data[self.team1[random.randint(0, 4)]]
            player2 = self.data[self.team2[random.randint(0, 4)]]
            if event <= 0.6: #SHOT
                if random.randint(1, 2) == 1: #Team1
                    player_xG = (player1.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        msg = await msg.edit(content=msg.content+"\nT1 Goal scored by {0}".format(player1.user.display_name))
                        self.score[0] = self.score[0] + 1
                else:                           #Team2
                    player_xG = (player2.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        msg = await msg.edit(content=msg.content+"\nT2 Goal scored by {0}".format(player2.user.display_name))
                        self.score[1] = self.score[1] + 1
            elif event <= 0.8: #HIT
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(player2.user.display_name, player1.user.display_name))
            elif event <= 0.9: #TAKEAWAY
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player2.user.display_name, player1.user.display_name))
            else:               #BLOCK
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player1.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player2.user.display_name))

        msg = await msg.edit(content=msg.content+"\nFinal Score: {0}-{1}".format(self.score[0], self.score[1]))


# xG could be first pick the distribution value, weight it by shot,
#  then take random.random() and if it lands on the range 1 - xG it is then a goal
# but what about other events like takeaways and hits? 
# maybe those should be their own random, and if number between range it will be a shot, takeaway, or a hit

# time of event
#missed shot messages


# edit the original message so no spam.......\n
# positions? passing plays a role in assists
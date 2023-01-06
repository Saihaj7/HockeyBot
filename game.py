import discord
from discord.ext import tasks
import random
import os
from dotenv import load_dotenv
#from time import sleep
from scipy.stats import truncnorm
from asyncio import sleep

# probability distribution for expected goals for shots that are taken, tried to get a semi realistic balance between shot totals and goals
def get_truncated_normal(mean=0, sd=1, low=0, upp=20):  
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        
xG = get_truncated_normal(mean=0.05, sd=0.1, low=0, upp=1)
#xG.rvs()

TEAMS = ['BOS', 'BUF', 'CAR', 'CBJ', 'DET', 'FLA', 'MTL', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'TBL', 'TOR', 'WSH',
        'ANA', 'ARI', 'CGY', 'CHI', 'COL', 'DAL', 'EDM', 'LAK', 'MIN', 'NSH', 'SEA', 'SJS', 'STL', 'VAN', 'VGK', 'WPG']

class Game:
    def __init__(self, players, data):
        self.score = [0, 0] # [0] = score for t1, [1] = score for t2
        self.shots = [0, 0] # ^^^
        self.data = data #dictionary
        self.team_names = random.sample(TEAMS, 2)
        if len(players) >= 12:
            self.team1 = players[:6]
            self.team2 = players[6:]                    # I feel like this could be way better, Team class?
            self.goalie1 = self.data[self.team1[-1]]
            self.goalie2 = self.data[self.team2[-1]]

    async def play(self, message):
        score = await message.channel.send("-----SCORE-----\n{4}: {0} --- {5}: {1}\n-----SHOTS-----\n{4}: {2} --- {5}: {3}".format(self.score[0], self.score[1], self.shots[0], self.shots[1], self.team_names[0], self.team_names[1]))
        clock = await message.channel.send("PERIOD 1: 20:00")
        await message.channel.send('------------------')
        roster1 = await message.channel.send("{6}\nF:   {0} - {1} - {2} \nD:   {3} - {4}\nG:   {5}".format(self.team1[0].display_name, self.team1[1].display_name, self.team1[2].display_name, self.team1[3].display_name, self.team1[4].display_name, self.team1[5].display_name, self.team_names[0]))
        roster2 = await message.channel.send("{6}\nF:   {0} - {1} - {2} \nD:   {3} - {4}\nG:   {5}".format(self.team2[0].display_name, self.team2[1].display_name, self.team2[2].display_name, self.team2[3].display_name, self.team2[4].display_name, self.team2[5].display_name, self.team_names[1]))
        #^^^^ left as var's for now in case I want to add emoji effects to players involved in events
        await message.channel.send('------------------')
        msg = await message.channel.send("The puck has been dropped between {0} and {1}!!!".format(self.team_names[0], self.team_names[1]))

        for minute in range(60): #event each minute
            #await sleep(1)
            clock = await clock.edit(content="PERIOD {0}: {1}:00".format(1 + minute // 20, 20 - minute % 20)) #GAME TIME
            event = random.random()      
            
            p1, p2 = random.randint(0, 4), random.randint(0, 4)
            player1 = self.data[self.team1[p1]] #grabs Player object   #team.py change; will grab from skaters i.e
            player2 = self.data[self.team2[p2]] #grabs Player object   # player1 = self.data[team.get_skaters()[random.randint(0, len(team.get_skaters) - 1)]]

            if event <= 0.8: #SHOT
                if random.randint(1, 2) == 1: #Team1
                    self.shots[0] = self.shots[0] + 1
                    player_xG = ((20 - self.goalie2.save_val()) / 10) * ((player1.shot_val() / 10) * xG.rvs()) # expected goal odds modified by shot value and the strength of the goalie
                    if random.random() < player_xG: #GOAL
                        one_assist = random.choices(self.team1[:5], weights=(self.data[self.team1[0]].pass_val(), self.data[self.team1[1]].pass_val(), self.data[self.team1[2]].pass_val(),
                                            self.data[self.team1[3]].pass_val(), self.data[self.team1[4]].pass_val()), k=1)
                        two_assist = random.choices(self.team1[:5], weights=(self.data[self.team1[0]].pass_val(), self.data[self.team1[1]].pass_val(), self.data[self.team1[2]].pass_val(),
                                            self.data[self.team1[3]].pass_val(), self.data[self.team1[4]].pass_val()), k=2) 
                        if self.team1[p1] not in two_assist and (two_assist[0] != two_assist[1]): #and random.random() < 0.4: # TWO ASSISTS
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0}, assisted by {1}, {3}:rotating_light:".format(player1.user.display_name, self.data[two_assist[0]].user.display_name, self.team_names[0], self.data[two_assist[1]].user.display_name))
                            self.score[0] = self.score[0] + 1
                        elif self.team1[p1] not in one_assist: #and random.random() < 0.8: # ONE ASSIST
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0}, assisted by {1}:rotating_light:".format(player1.user.display_name, self.data[one_assist[0]].user.display_name, self.team_names[0]))
                            self.score[0] = self.score[0] + 1
                        else: #UNASSISTED
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{1} Goal scored by {0}:rotating_light:".format(player1.user.display_name, self.team_names[0]))
                            self.score[0] = self.score[0] + 1
                    
                else:                           #Team2
                    self.shots[1] = self.shots[1] + 1
                    player_xG = ((20 - self.goalie1.save_val()) / 10) * ((player2.shot_val() / 10) * xG.rvs()) # expected goal odds modified by shot value and the strength of the goalie
                    if random.random() < player_xG: #GOAL
                        one_assist = random.choices(self.team2[:5], weights=(self.data[self.team2[0]].pass_val(), self.data[self.team2[1]].pass_val(), self.data[self.team2[2]].pass_val(),
                                            self.data[self.team2[3]].pass_val(), self.data[self.team2[4]].pass_val()), k=1)
                        two_assist = random.choices(self.team2[:5], weights=(self.data[self.team2[0]].pass_val(), self.data[self.team2[1]].pass_val(), self.data[self.team2[2]].pass_val(),
                                            self.data[self.team2[3]].pass_val(), self.data[self.team2[4]].pass_val()), k=2) 
                        if self.team2[p2] not in two_assist and (two_assist[0] != two_assist[1]): #and random.random() < 0.4: # TWO ASSISTS
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0}, assisted by {1}, {3}:rotating_light:".format(player2.user.display_name, self.data[two_assist[0]].user.display_name, self.team_names[1], self.data[two_assist[1]].user.display_name))
                            self.score[1] = self.score[1] + 1
                        elif self.team2[p2] not in one_assist: #and random.random() < 0.8: # ONE ASSIST
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0}, assisted by {1}:rotating_light:".format(player2.user.display_name, self.data[one_assist[0]].user.display_name, self.team_names[1]))
                            self.score[1] = self.score[1] + 1
                        else: #UNASSISTED
                            msg = await msg.edit(content=msg.content+"\n:rotating_light:{1} Goal scored by {0}:rotating_light:".format(player2.user.display_name, self.team_names[1]))
                            self.score[1] = self.score[1] + 1
                    
                score = await score.edit(content="-----SCORE-----\n{4}: {0} --- {5}: {1}\n-----SHOTS-----\n{4}: {2} --- {5}: {3}".format(self.score[0], self.score[1], self.shots[0], self.shots[1], self.team_names[0], self.team_names[1]))

            elif event <= 0.9: #HIT
                if random.randint(1, 2) == 1: #Team1
                    player = random.choices(self.team1[:5], weights=(self.data[self.team1[0]].strength_val(), self.data[self.team1[1]].strength_val(), self.data[self.team1[2]].strength_val(),
                                            self.data[self.team1[3]].strength_val(), self.data[self.team1[4]].strength_val()), k=1)
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(self.data[player[0]].user.display_name, player2.user.display_name))
                else: #TEAM2
                    player = random.choices(self.team2[:5], weights=(self.data[self.team2[0]].strength_val(), self.data[self.team2[1]].strength_val(), self.data[self.team2[2]].strength_val(),
                                            self.data[self.team2[3]].strength_val(), self.data[self.team2[4]].strength_val()), k=1)
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(self.data[player[0]].user.display_name, player1.user.display_name))
            elif event <= 0.95: #TAKEAWAY
                if random.randint(1, 2) == 1: #Team1
                    player = random.choices(self.team1[:5], weights=(self.data[self.team1[0]].strength_val(), self.data[self.team1[1]].strength_val(), self.data[self.team1[2]].strength_val(),
                                            self.data[self.team1[3]].strength_val(), self.data[self.team1[4]].strength_val()), k=1)
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(self.data[player[0]].user.display_name, player2.user.display_name))
                else: #TEAM2
                    player = random.choices(self.team2[:5], weights=(self.data[self.team2[0]].strength_val(), self.data[self.team2[1]].strength_val(), self.data[self.team2[2]].strength_val(),
                                            self.data[self.team2[3]].strength_val(), self.data[self.team2[4]].strength_val()), k=1)
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(self.data[player[0]].user.display_name, player1.user.display_name))
            else:               #BLOCK
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player1.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player2.user.display_name))
        #FINAL MESSAGES
        clock = await clock.edit(content="PERIOD 3: 00:00")
        msg = await msg.edit(content=msg.content+"\n\nFinal Score: {0}-{1}".format(self.score[0], self.score[1]))
        msg = await msg.edit(content=msg.content+"\nShot Totals: {0}-{1}".format(self.shots[0], self.shots[1]))


      # scaled by att


      #random.choices() for weighted player selection, https://pynative.com/python-weighted-random-choices-with-probability/
      # event then take player?

      #new xG dist for D men so that they score less compared to forwards
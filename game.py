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
        
xG = get_truncated_normal(mean=0.05, sd=0.1, low=0, upp=1)
#xG.rvs()

TEAMS = ['BOS', 'BUF', 'CAR', 'CBJ', 'DET', 'FLA', 'MTL', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'TBL', 'TOR', 'WSH',
        'ANA', 'ARI', 'CGY', 'CHI', 'COL', 'DAL', 'EDM', 'LAK', 'MIN', 'NSH', 'SEA', 'SJS', 'STL', 'VAN', 'VGK', 'WPG']

class Game:
    def __init__(self, players, data):
        #self.players = players
        #self.players = []
        self.score = [0, 0] # [0] = score for t1, [1] = score for t2
        self.shots = [0, 0] # ^^^
        self.data = data
        self.team_names = random.sample(TEAMS, 2)
        if len(players) >= 12:
            self.team1 = players[:6]
            self.team2 = players[6:]
            self.goalie1 = self.data[self.team1[-1]]
            self.goalie2 = self.data[self.team2[-1]]

    async def play(self, message):
        score = await message.channel.send("-----SCORE-----\n{4}: {0} --- {5}: {1}\n-----SHOTS-----\n{4}: {2} --- {5}: {3}".format(self.score[0], self.score[1], self.shots[0], self.shots[1], self.team_names[0], self.team_names[1]))
        clock = await message.channel.send("PERIOD 1: 20:00")
        await message.channel.send('------------------')
        roster1 = await message.channel.send("{6}\nF:   {0} - {1} - {2} \nD:   {3} - {4}\nG:   {5}".format(self.team1[0].display_name, self.team1[1].display_name, self.team1[2].display_name, self.team1[3].display_name, self.team1[4].display_name, self.team1[5].display_name, self.team_names[0]))
        roster2 = await message.channel.send("{6}\nF:   {0} - {1} - {2} \nD:   {3} - {4}\nG:   {5}".format(self.team2[0].display_name, self.team2[1].display_name, self.team2[2].display_name, self.team2[3].display_name, self.team2[4].display_name, self.team2[5].display_name, self.team_names[1]))
        
        await message.channel.send('------------------')
        msg = await message.channel.send("The puck has been dropped between {0} and {1}!!!".format(self.team_names[0], self.team_names[1]))
        for minute in range(60): #event each minute
            #await sleep(1)
            clock = await clock.edit(content="PERIOD {0}: {1}:00".format(1 + minute // 20, 20 - minute % 20))
            event = random.random()                                     
            player1 = self.data[self.team1[random.randint(0, 4)]] #grabs Player object
            player2 = self.data[self.team2[random.randint(0, 4)]] #grabs Player object
            if event <= 0.85: #SHOT
                if random.randint(1, 2) == 1: #Team1
                    self.shots[0] = self.shots[0] + 1
                    player_xG = (player1.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0} on {1}:rotating_light:".format(player1.user.display_name, self.goalie2.user.display_name, self.team_names[0]))
                        self.score[0] = self.score[0] + 1
                    
                else:                           #Team2
                    self.shots[1] = self.shots[1] + 1
                    player_xG = (player2.shot_val() / 10) * xG.rvs()
                    if random.random() < player_xG: #GOAL
                        msg = await msg.edit(content=msg.content+"\n:rotating_light:{2} Goal scored by {0} on {1}:rotating_light:".format(player2.user.display_name, self.goalie1.user.display_name, self.team_names[1]))
                        self.score[1] = self.score[1] + 1
                    
                score = await score.edit(content="-----SCORE-----\n{4}: {0} --- {5}: {1}\n-----SHOTS-----\n{4}: {2} --- {5}: {3}".format(self.score[0], self.score[1], self.shots[0], self.shots[1], self.team_names[0], self.team_names[1]))
            elif event <= 0.9: #HIT
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} hit {1}".format(player2.user.display_name, player1.user.display_name))
            elif event <= 0.95: #TAKEAWAY
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player1.user.display_name, player2.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} took the puck away from {1}".format(player2.user.display_name, player1.user.display_name))
            else:               #BLOCK
                if random.randint(1, 2) == 1: #Team1
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player1.user.display_name))
                else: #TEAM2
                    msg = await msg.edit(content=msg.content+"\n{0} blocked a shot!".format(player2.user.display_name))

        clock = await clock.edit(content="PERIOD 3: 00:00")
        msg = await msg.edit(content=msg.content+"\n\nFinal Score: {0}-{1}".format(self.score[0], self.score[1]))
        msg = await msg.edit(content=msg.content+"\nShot Totals: {0}-{1}".format(self.shots[0], self.shots[1]))


# xG could be first pick the distribution value, weight it by shot,
#  then take random.random() and if it lands on the range 1 - xG it is then a goal
# but what about other events like takeaways and hits? 
# maybe those should be their own random, and if number between range it will be a shot, takeaway, or a hit


# positions? passing plays a role in assists

#fights 
#powerplays
#edit play by play messages

#assists
#periods?
#rosters into a single message
#CLOCK IN SCOREBOARD


# on play() return it gives you stats then they can enter stats request
#Overtime

# $event to see wall of text
#goalie pulls


#stay tuned for a 7pm puck drop!! message
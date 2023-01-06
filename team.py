import discord
import random
import os
from dotenv import load_dotenv
from scipy.stats import truncnorm

class Team: #rough class outline for later if needed

    def __init__(self, players, goalie, name):
        if len(players) == 6:
            self.players = players
        self.state = 5 #players on the ice, don't forget to change event odds depending on game state, i.e. make shots unlikely for pk team, opposite for pp team
        self.goalie = goalie
        self.skaters = players[:5] # self.players exluding those in penalty box and goalie
        self.name = name

    def get_players(self):
        return self.players

    def get_skaters(self):
        return self.skaters

    def get_state(self):
        return self.state

    def get_goalie(self):
        return self.goalie

    def toggle_penalty(self, player):
        if player not in self.skating: #returns player 
            self.skating.append(player)
            self.state = self.state + 1
        elif self.state >= 3:           #put player in the penalty box (i.e. makes them unavailable for event selection)
            self.skating.remove(player)
            self.state = self.state - 1

    def goalie_pull(self):
        self.skating.append(self.goalie)
        self.state = self.state + 1
    
    def goalie_return(self):
        self.skating.remove(self.goalie)
        self.state = self.state - 1
import discord
import random
import os
from dotenv import load_dotenv
from scipy.stats import truncnorm

class Team:

    def __init__(self, players, goalie):
        if len(players) == 6:
            self.players = players
        self.state = 5 #players on the ice
        self.goalie = goalie

    def get_players(self):
        return self.players

    def get_state(self):
        return self.state

    def get_goalie(self):
        return self.goalie
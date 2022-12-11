import discord
import random
import os
from dotenv import load_dotenv


class Game:

    def __init__(self, players):
        self.players = players
        if len(players) == 10:
            self.team1 = players[:5]
            self.team2 = players[5:]
            

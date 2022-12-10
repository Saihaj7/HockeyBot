import discord
import bot
import random
import os
from dotenv import load_dotenv

class Player:
    def __init__(self, name, stats):
        self.name = name
        self.stats = {'shot': random.randint(1, 20)}

    def reroll(self):
        self.stats['stats'] = random.randint(1, 20)


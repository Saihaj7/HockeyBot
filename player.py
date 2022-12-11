import discord
import random
import os
from dotenv import load_dotenv

class Player:
    def __init__(self, user):
        self.user = user
        self.stats = {'shot': random.randint(1, 20)}

    def reroll(self):
        self.stats['shot'] = random.randint(1, 20)

    def __repr__(self):
        return "Player: {0}, Shot: {1}".format(self.user, self.stats['shot'])

    def __str__(self):
        return self.user.name
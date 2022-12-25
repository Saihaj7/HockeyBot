import discord
import random
import os
from dotenv import load_dotenv
from scipy.stats import truncnorm


def get_truncated_normal(mean=0, sd=1, low=0, upp=20):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        
X = get_truncated_normal(mean=10, sd=2, low=1, upp=20)
#X.rvs()


class Player:
    def __init__(self, user):
        self.user = user
        self.atts = {'shot': int(X.rvs()), 'save': int(X.rvs()), 'passing': int(X.rvs())}

    def reroll(self):
        self.atts['shot'] = int(X.rvs())
        #self.atts['shot'] = random.randint(1, 20)
    def shot_val(self):
        return self.atts['shot']

    def __repr__(self):
        return "Player: {0}, Shot: {1}".format(self.user, self.atts['shot'])

    def __str__(self):
        return self.user.name
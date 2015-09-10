# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
Foo
"""


source_code = ""


bibliography = ()


links = {}


keywords = ()

class Constants:
    name_in_url = 't1_ua'
    players_per_group = 2
    num_rounds = 1


class Subsession(otree.models.BaseSubsession):

    v1 = models.CurrencyField(min=0, max=10)
    v2 = models.CurrencyField(min=0, max=10)
    v3 = models.CurrencyField(min=0, max=10)

    def random_money(self, offset, limit):
        value = random.randint(offset, limit)
        if value < limit:
            value += random.random()
        return value

    def before_session_starts(self):
        self.match_players("perfect_strangers")
        self.v3 = self.random_money(0, 10)
        self.v2 = self.random_money(self.v3, 10)
        self.v1 = self.random_money(self.v2, 10)


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    clearingprice = models.CurrencyField(min=0, max=10)

    def set_payoff(self):
        bid_x_players = []
        for p in self.get_players():
            bid_x_players.append((p.bid_1, p, 1))
            bid_x_players.append((p.bid_2, p, 2)
        bid_x_players.sort(lambda bxp: bxp[0], reverse_true)
        self.clearingprice = bid_x_players[-1][0]
        for idx, bxp in enumerate(bid_x_players[:-1]):
            vidx = idx + 1  # vidx contains if won item 1, 2 or 3
            player, bid_number = bxp[1], bxp[2]  # bid number is the what bid make this player winner
            if bid_number == 1:  # win with bid 1
                player.win_1 = True
                if vidx == 1:  # win the item 1 with bid 1
                    player.profits_1 = self.subsession.v1 -  self.clearingprice
                elif vidx == 2:  # win the item 2 with bid 1
                    player.profits_1 = self.subsession.v2 -  self.clearingprice
                elif vidx == 3:  # win the item 3 with bid 1
                    player.profits_1 = self.subsession.v3 -  self.clearingprice
                player.payoff = (player.payoff or 0) + player.profits_1
            elif bid_number == 2:  # win with bid 2
                player.win_2 = True
                if vidx == 1:
                    player.profits_2 = self.subsession.v1 -  self.clearingprice
                elif vidx == 2:
                    player.profits_2 = self.subsession.v2 -  self.clearingprice
                elif vidx == 3:
                    player.profits_2 = self.subsession.v3 -  self.clearingprice
                player.payoff = (player.payoff or 0) + player.profits_2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_1 = models.CurrencyField(min=0, max=10, verbose_name="Your First Bid")
    bid_2 = models.CurrencyField(min=0, max=10, verbose_name="Your Second Bid")
    profits_1 = models.CurrencyField(default=0)
    profits_2 = models.CurrencyField(default=0)
    win_1 = models.BooleanField(default=False)
    win_2 = models.BooleanField(default=False)







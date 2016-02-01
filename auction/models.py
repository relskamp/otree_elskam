# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

import math

from django.conf import settings

from . import match_players


doc = """
Foo
"""


source_code = "https://github.com/leliel12/otree_elskam"


bibliography = ()


links = {}

keywords = ()

class Constants:
    name_in_url = 'auction'
    players_per_group = None
    num_rounds = 15
    start_money = c(settings.SESSION_CONFIG_DEFAULTS["participation_fee"])
    players_per_group_t1 = 2
    players_per_group_t2 = 3


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        players = self.get_players()
        if self.round_number == 1:
            players_per_group = (
                Constants.players_per_group_t1
                if self.session.config['treatment'].startswith("T1-") else
                Constants.players_per_group_t2)
            groups = [
                players[i:i+players_per_group]
                for i in xrange(0, len(players), players_per_group)]
            self.set_groups(groups)
        else:
            self.match_players("perfect_strangers")
        for player in players:
            player.set_values()


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    clearingprice = models.CurrencyField()

    def set_round_profit(self):
        treatment = self.session.config['treatment']

        bid_x_players = []
        player_values = {}
        players = self.get_players()
        for player in players:
            # bid - random factor - player - bid number
            rf = [random.random(), random.random(), random.random()]
            bid_x_players.append((player.bid_1, rf.pop(), player, 1))
            bid_x_players.append((player.bid_2, rf.pop(), player, 2))
            if treatment.startswith("T2-"):
                bid_x_players.append((player.bid_3, rf.pop(), player, 3))
            player_values[player] = list(player.values())

        bid_x_players.sort(key=lambda bxp: tuple(bxp[0:1]), reverse=True)

        if treatment.endswith("-UA"):
            self.clearingprice = bid_x_players[-1][0]

        for idx, bxp in enumerate(bid_x_players[:-1]):
            item = idx + 1  # vidx contains if won item 1, 2 or 3

            # bid number is the what bid make this player winner
            bid, player, bid_number = bxp[0], bxp[2], bxp[3]
            values = player_values[player]
            cost = self.clearingprice if treatment.endswith("-UA") else bid

            if bid_number == 1:
                player.win_bid_1 = True
                player.item_win_bid_1 = item
                player.profits_bid_1 = values.pop(0) - cost
                player.round_profit = (player.round_profit or 0) + player.profits_bid_1
            elif bid_number == 2:
                player.win_bid_2 = True
                player.item_win_bid_2 = item
                player.profits_bid_2 = values.pop(0) - cost
                player.round_profit = (player.round_profit or 0) + player.profits_bid_2
            elif bid_number == 3:
                player.win_bid_3 = True
                player.item_win_bid_3 = item
                player.profits_bid_3 = values.pop(0) - cost
                player.round_profit = (player.round_profit or 0) + player.profits_bid_3


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_1 = models.CurrencyField(min=0, max=100, verbose_name="Your First Bid")
    bid_2 = models.CurrencyField(min=0, max=100, verbose_name="Your Second Bid")
    bid_3 = models.CurrencyField(min=0, max=100, verbose_name="Your Third Bid")
    profits_bid_1 = models.CurrencyField(default=0)
    profits_bid_2 = models.CurrencyField(default=0)
    profits_bid_3 = models.CurrencyField(default=0)
    win_bid_1 = models.BooleanField(default=False)
    win_bid_2 = models.BooleanField(default=False)
    win_bid_3 = models.BooleanField(default=False)
    item_win_bid_1 = models.PositiveIntegerField()
    item_win_win_2 = models.PositiveIntegerField()
    item_win_win_3 = models.PositiveIntegerField()

    v1 = models.CurrencyField(min=0, max=100)
    v2 = models.CurrencyField(min=0, max=100)
    v3 = models.CurrencyField(min=0, max=100)

    round_profit = models.CurrencyField()
    payoff_rounds_numbers = models.TextField()

    def values(self):
        if self.session.config['treatment'].startswith("T1-"):
            return self.v1, self.v2
        return self.v1, self.v2, self.v3

    def set_values(self):
        if self.session.config['treatment'].startswith("T1-"):
            v2 = random.randint(0, 1000)
            v1 = random.randint(v2, 1000)
            self.v2, self.v1 = map(lambda x: x / 10., [v2, v1])
        else:
            v3 = random.randint(0, 1000)
            v2 = random.randint(v3, 1000)
            v1 = random.randint(v2, 1000)
            self.v3, self.v2, self.v1 = map(lambda x: x / 10., [v3, v2, v1])

    def str_payoff(self):
        pre = u"- " if self.payoff < 0 else u""
        return pre + unicode(c(abs(self.payoff)))

    def str_round_profit(self):
        pre = u"- " if self.round_profit < 0 else u""
        return pre + unicode(c(abs(self.round_profit)))

    def list_payoff_rounds_numbers(self):
        return map(int, self.payoff_rounds_numbers.split(","))

    def final_payoff(self):
        return self.payoff + Constants.start_money

    def set_payoff(self):
        in_all_rounds = self.in_all_rounds()
        random.shuffle(in_all_rounds)

        choices_rns, choices_payoff = [], 0
        for c in in_all_rounds[:2]:
            choices_payoff += c.round_profit
            choices_rns.append(c.round_number)
        choices_rns.sort()

        self.payoff = (choices_payoff)/10
        self.payoff_rounds_numbers = ",".join(map(str, choices_rns))

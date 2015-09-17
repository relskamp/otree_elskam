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

import common


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
    start_money = c(5)
    num_rounds = settings.ELSKAM["t1_rounds"]


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        self.match_players("perfect_strangers")
        for player in self.get_players():
            player.set_values()


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    clearingprice = models.CurrencyField()

    def set_payoffs(self):
        bid_x_players = []
        player_values = {}
        players = self.get_players()
        for player in players:
            rf1, rf2 = random.random(), random.random()
            # bid - random factor - player - bid number
            bid_x_players.append((player.bid_1, rf1, player, 1))
            bid_x_players.append((player.bid_2, rf2, player, 2))
            player_values[player] = [player.v1, player.v2]

        bid_x_players.sort(key=lambda bxp: bxp[0:2], reverse=True)
        self.clearingprice = bid_x_players[-1][0]
        for idx, bxp in enumerate(bid_x_players[:-1]):
            item = idx + 1  # vidx contains if won item 1, 2 or 3
            player, bid_number = bxp[2], bxp[3]  # bid number is the what bid make this player winner
            values = player_values[player]
            if bid_number == 1:
                player.win_bid_1 = True
                player.item_win_bid_1 = item
                player.profits_bid_1 = values.pop(0) - self.clearingprice
                player.payoff = (player.payoff or 0) + player.profits_bid_1
            elif bid_number == 2:
                player.win_bid_2 = True
                player.item_win_bid_2 = item
                player.profits_bid_2 = values.pop(0) - self.clearingprice
                player.payoff = (player.payoff or 0) + player.profits_bid_2

        for player in players:
            player.total_payoff = player.payoff
            if self.subsession.round_number == 1:
                player.total_payoff += Constants.start_money
            else:
                for pplayer in player.in_previous_rounds():
                    player.total_payoff += pplayer.total_payoff


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_payoff = models.CurrencyField()

    bid_1 = models.CurrencyField(min=0, max=10, verbose_name="Your First Bid")
    bid_2 = models.CurrencyField(min=0, max=10, verbose_name="Your Second Bid")
    profits_bid_1 = models.CurrencyField(default=0)
    profits_bid_2 = models.CurrencyField(default=0)
    win_bid_1 = models.BooleanField(default=False)
    win_bid_2 = models.BooleanField(default=False)
    item_win_bid_1 = models.PositiveIntegerField()
    item_win_win_2 = models.PositiveIntegerField()

    v1 = models.CurrencyField(min=0, max=10)
    v2 = models.CurrencyField(min=0, max=10)

    final_payoff = models.CurrencyField()
    final_payoff_round_number = models.PositiveIntegerField()

    def values(self):
        return self.v1, self.v2

    def set_values(self):
        self.v2 = common.random_money(0, 10)
        self.v1 = common.random_money(self.v2, 10)

    def balance(self):
        if not hasattr(self, "__balance"):
            if self.round_number == 1:
                self.__balance = Constants.start_money
            else:
                rnm1 = self.round_number - 1
                for p in self.in_previous_rounds():
                    if p.round_number == rnm1:
                        self.__balance = p.total_payoff
        return self.__balance

    def str_balance(self):
        balance = self.balance()
        pre = u"- " if balance < 0 else u""
        return pre + unicode(c(abs(balance)))

    def str_payoff(self):
        pre = u"- " if self.payoff < 0 else u""
        return pre + unicode(c(abs(self.payoff)))

    def str_total_payoff(self):
        pre = u"- " if self.total_payoff < 0 else u""
        return pre + unicode(c(abs(self.total_payoff)))

    def str_final_payoff(self):
        pre = u"- " if self.final_payoff < 0 else u""
        return pre + unicode(c(abs(self.final_payoff)))

    def set_final_payoff(self):
        choiced = random.choice(self.in_all_rounds())
        participant = choiced.participant
        choiced_payoff = choiced.payoff
        choiced_rn = choiced.round_number
        Player.objects.filter(participant=participant).update(
            final_payoff=choiced_payoff, final_payoff_round_number=choiced_rn)



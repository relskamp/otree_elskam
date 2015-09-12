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
    name_in_url = 't1_da'
    players_per_group = 2
    num_rounds = 1
    start_money = c(5)
    num_rounds = settings.ELSKAM["t1_rounds"]


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        self.match_players("perfect_strangers")


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    v1 = models.CurrencyField(min=0, max=10)
    v2 = models.CurrencyField(min=0, max=10)
    v3 = models.CurrencyField(min=0, max=10)

    def set_payoffs(self):
        self.v3 = common.random_money(0, 10)
        self.v2 = common.random_money(self.v3, 10)
        self.v1 = common.random_money(self.v2, 10)

        bid_x_players = []
        players = self.get_players()
        for p in players:
            rf1, rf2 = random.random(), random.random()
            # bid - random factos - player - bid number
            bid_x_players.append((p.bid_1, rf1, p, 1))
            bid_x_players.append((p.bid_2, rf2, p, 2))
        bid_x_players.sort(key=lambda bxp: bxp[0:2], reverse=True)

        for idx, bxp in enumerate(bid_x_players[:-1]):
            vidx = idx + 1  # vidx contains if won item 1, 2 or 3

            bid, player, bid_number = bxp[0], bxp[2], bxp[3]  # bid number is the what bid make this player winner
            if bid_number == 1:  # win with bid 1
                player.win_1 = True
                if vidx == 1:  # win the item 1 with bid 1
                    player.profits_1 = self.v1 -  bid
                    player.bid_1_win_value = self.v1
                elif vidx == 2:  # win the item 2 with bid 1
                    player.profits_1 = self.v2 -  bid
                    player.bid_1_win_value = self.v2
                elif vidx == 3:  # win the item 3 with bid 1
                    player.profits_1 = self.v3 -  bid
                    player.bid_1_win_value = self.v3
                player.payoff = (player.payoff or 0) + player.profits_1
            elif bid_number == 2:  # win with bid 2
                player.win_2 = True
                if vidx == 1:
                    player.profits_2 = self.v1 - bid
                    player.bid_2_win_value = self.v1
                elif vidx == 2:
                    player.profits_2 = self.v2 - bid
                    player.bid_2_win_value = self.v2
                elif vidx == 3:
                    player.profits_2 = self.v3 -  bid
                    player.bid_2_win_value = self.v3
                player.payoff = (player.payoff or 0) + player.profits_2

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
    profits_1 = models.CurrencyField(default=0)
    profits_2 = models.CurrencyField(default=0)
    win_1 = models.BooleanField(default=False)
    win_2 = models.BooleanField(default=False)
    bid_1_win_value = models.CurrencyField(default=0)
    bid_2_win_value = models.CurrencyField(default=0)

    final_payoff = models.CurrencyField()
    final_payoff_round_number = models.PositiveIntegerField()

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
        choiced_rn = choiced.subsession.round_number
        Player.objects.filter(participant=participant).update(
            final_payoff=choiced_payoff, final_payoff_round_number=choiced_rn)

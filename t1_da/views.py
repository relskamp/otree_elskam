# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):
    return {}


class Decide(Page):

    form_model = models.Player
    form_fields = ["bid_1", "bid_2"]


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def vars_for_template(self):
        results = []
        for player in self.group.get_players():
            results.append({
                "bidder": player,
                "is_you": player == self.player,
                "bid": player.bid_1,
                "value": player.bid_1_win_value,
                "won": player.win_1})
            results.append({
                "bidder": player,
                "is_you": player == self.player,
                "bid": player.bid_2,
                "value": player.bid_2_win_value,
                "won": player.win_2})
        results.sort(key=lambda r: r["bid"], reverse=True)
        return {"results": results}


page_sequence = [Decide, ResultsWaitPage, Results]

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
                "value": player.v1,
                "won": player.win_bid_1,
                "extra_bid": (
                    "" if player.win_bid_1 else
                    "<small><code>Market Price</code><small>")})
            results.append({
                "bidder": player,
                "is_you": player == self.player,
                "bid": player.bid_2,
                "value": player.v2,
                "won": player.win_bid_2,
                "extra_bid": (
                    "" if player.win_bid_2 else
                    "<small><code>Market Price</code><small>")})

        results.sort(key=lambda r: (r["bid"], r["won"]), reverse=True)
        return {"results": results}

    def before_next_page(self):
        if self.subsession.round_number == Constants.num_rounds:
            self.player.set_final_payoff()


class Resume(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [Decide, ResultsWaitPage, Results, Resume]

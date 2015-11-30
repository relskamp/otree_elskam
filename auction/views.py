# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):
    return {"treatment": self.session.config['treatment']}


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class AssignmentRulesAndProfitCalculations(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class IllustrativeExamples(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class AdditionalRemarks(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Decide(Page):

    form_model = models.Player

    def get_form_fields(self):
        if self.session.config['treatment'].startswith("T1-"):
            return ["bid_1", "bid_2"]
        return ["bid_1", "bid_2", "bid_3"]

    def error_message(self, values):
        if values["bid_2"] > values["bid_1"]:
            return "Your second bid must be less than or equal to first one"
        if self.session.config['treatment'].startswith("T2-"):
            if values["bid_3"] > values["bid_2"]:
                return "Your third bid must be less than or equal to second one"


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_round_profit()


class Results(Page):

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        results = []
        for player in self.group.get_players():
            results.append({
                "bidder": player,
                "is_you": player == self.player,
                "bid": player.bid_1,
                "value": player.v1,
                "won": player.win_bid_1})
            results.append({
                "bidder": player,
                "is_you": player == self.player,
                "bid": player.bid_2,
                "value": player.v2,
                "won": player.win_bid_2})
            if treatment.startswith("T2-"):
                results.append({
                    "bidder": player,
                    "is_you": player == self.player,
                    "bid": player.bid_3,
                    "value": player.v3,
                    "won": player.win_bid_3})

        if treatment.endswith("-UA"):
            for d in results:
                d["extra_bid"] = (
                    "" if d["won"] else
                    "<small><code>Market Price</code><small>")

        results.sort(key=lambda r: (r["bid"], r["won"]), reverse=True)
        return {"results": results}

    def before_next_page(self):
        if self.subsession.round_number == Constants.num_rounds:
            self.player.set_payoff()


class Resume(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [
    Introduction,
    AssignmentRulesAndProfitCalculations,
    IllustrativeExamples,
    AdditionalRemarks,
    Decide, ResultsWaitPage, Results, Resume]

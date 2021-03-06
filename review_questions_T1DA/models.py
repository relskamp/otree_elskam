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
    name_in_url = 'part1'
    players_per_group = None
    num_rounds = 1
    payoff = c(5)
   



class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    Q1 = models.CharField(
        max_length=255, choices=['One', 'Two', 'Three'],
        verbose_name="How many bids will you submit in each auction round?",
        widget=widgets.RadioSelect())

    Q2 = models.CharField(
        max_length=255,
        choices=[
            "No", "Yes"],
        verbose_name="Will your valuations be drawn anew before each auction round?",
        widget=widgets.RadioSelect())


    Q3 = models.CharField(
        verbose_name=(
            "Are your valuations independent of the valuations assigned to your competitor?"),
        max_length=255, widget=widgets.RadioSelect(),
        choices=[
            "Yes", "No" ])

    Q4 = models.CharField(
        verbose_name=" How are your valuations determined?",
        choices=[
            "The valuation on the second unit (v2) is randomly drawn between 0 and 100, and the value on the first unit (v1) is drawn randomly from the interval between v2 and 100.",
                 "Valuations are same across all 25 auction rounds",
            "Valuations are linked to bids in the last round"],
        max_length=255, widget=widgets.RadioSelect())

    Q5 = models.CharField(
        verbose_name="If you win an item, what price do you pay?",
        widget=widgets.RadioSelect(), max_length=255,
        choices=["My bid corresponding to the unit won",
                 "The market price  determined by the losing bid - the fourth highest bid",
                 "My competitor's highest bid"])

    Q6 = models.CharField(
        verbose_name=(
            "How many units are your guaranteed to purchase?"),
        widget=widgets.RadioSelect(), max_length=255,
        choices=["Zero", "One", "Two"])

    Q7 = models.CharField(
          verbose_name=(
            "Calculate the profits earned by Bidder A on her first unit purchased in the example depicted in the table below"),
          widget=widgets.RadioSelect(), max_length=255,
          choices=["98 - 15 = 83", "98 - 98 = 0", "98 - 45 = 54"])


    Q8 = models.CharField(
          verbose_name=(
              "Calculate the total profits earned by Bidder B on all units purchased in the example depicted in the table below"),
          widget=widgets.RadioSelect(), max_length=255,
          choices=["(56 - 56)+(48 - 48) = 0", "(56 - 36)+(48 - 20) = 48", "(56 - 48)+(48 - 48) = 8"])
    










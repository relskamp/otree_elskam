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
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1
    payoff = c(5)
    gambles_payoff = [
        (c(2.80), c(2.80)), (c(2.40), c(3.60)), (c(2.00), c(4.20)),
        (c(1.60), c(5.20)), (c(1.20), c(6.00)),(c(0.20), c(7.00)),
    ]
    ethnicities = [
        "Aboriginal/First Nations/Metis",
        "White/European",
        "Black/African/Caribbean",
        "Southeast Asian (e.g., Chinese, Japanese, Korean, Vietnamese, Cambodian,Filipino.etc)",
        "Arab (Saudi Arabian, Palestinian, Iraqi, etc)",
        "South Asian (East Indian, Sri Lankan, etc)",
        "Latin American (Costa Rican, Guatemalan, Brazilian, Columbian, etc)",
        "West Asian (Iranian, Afghani, etc)",
    ]


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

    gender = models.CharField(
        max_length=255, choices=['Female', 'Male', 'Other', 'Decline'],
        verbose_name="What gender do you identify with?",
        widget=widgets.RadioSelect())

    age = models.CharField(
        max_length=255,
        choices=[
            "under 18 years old", "18-20 years old", "21-22 years old",
            "23-25 years old", "over 25 years old"],
        verbose_name="What is your age?",
        widget=widgets.RadioSelect())

    ethnicity = models.TextField(
        widget=widgets.HiddenInput(),
        verbose_name="Which of the following BEST describes your ethnic background? Please TICK ALL THAT APPLY.")

    education_level = models.CharField(
        verbose_name=(
            "What is the highest degree or level of school you have completed?"
            " If currently enrolled, highest degree received."),
        max_length=255, widget=widgets.RadioSelect(),
        choices=[
            "High school graduate, diploma or the equivalent",
            "Some college credit, no degree",
            "Trade/technical/vocational training", "Bachelors degree",
            "Masters degree", "Other"])

    marital_status = models.CharField(
        verbose_name="What is your marital status?",
        choices=[
            "Single, never married", "Married or domestic partnership",
            "Other"],
        max_length=255, widget=widgets.RadioSelect())

    employment_status = models.CharField(
        verbose_name="What is your current employment status?",
        widget=widgets.RadioSelect(), max_length=255,
        choices=["no-job", "part-time", "full-time"])

    student_status = models.CharField(
        verbose_name=(
            "What is your current student status at the University of Guelph?"),
        widget=widgets.RadioSelect(), max_length=255,
        choices=["part-time", "full-time", "co-op", "other"])

    enrolled_type = models.CharField(
        verbose_name=(
            "What type of program are you enrolled in at the University of Guelph?"),
        widget=widgets.RadioSelect(), max_length=255,
        choices=["undergraduate degree", "graduate degree", "other"])
        
        
        
    major_type = models.CharField(
        verbose_name=(
           "Which College at the University of Guelph are you registered with?"),
       widget=widgets.RadioSelect(), max_length=255,
       choices=[" College of Business and Economics", "College of Physical and Engineering Science",  "College of Social and Applied Human Sciences","Ontario Agricultural College","Other"])


    class_type = models.CharField(
        verbose_name=(
            "How many Business and Economics classes have you taken so far (including those you are currently taking)?"),
        widget=widgets.RadioSelect(), max_length=255,
        choices=["0","Between 1 and 2", "Between 3 and 5", "Between 6 and 10", "More than 10"])


    auction_buy = models.CharField(
        verbose_name="Do you typically use auctions to buy goods?",
        widget=widgets.RadioSelect(), max_length=255,
        choices=["never", "occasionally", "frequently"])

    auctions_experience = models.CharField(
        verbose_name="How would you rate you previous experience with auctions?",
        widget=widgets.RadioSelect(), max_length=255,
        choices=[
            "no previous experience with auctions",
            "occasional use of auctions", "frequent use of auctions"])
            
    competitive_type = models.CharField(
        verbose_name=(
          "Evaluate the following statement: `When I play games for enjoyment, winning is very important to me' "),
        widget=widgets.RadioSelect(), max_length=255,
        choices=["I strongly disagree", "I disagree", "I neither disagree or agree", "I agree", "I strongly agree"])

            
            
           

    gamble = models.PositiveIntegerField(min=1, max=5)




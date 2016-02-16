# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role(),
            "treatment": self.session.config['treatment']}


class FirstPage(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class SecondPage(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1



class Introduction_1(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1

class Introduction_2(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1


class AssignmentRulesAndProfitCalculations(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1


class IllustrativeExamplesPart1Section1(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1


class IllustrativeExamplesPart1Section2(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1


class IllustrativeExamplesPart1Section3(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1


class IllustrativeExamplesPart1Section4(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1

class IllustrativeExamplesPart2(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1

class IllustrativeExamplesPart3(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1

class IllustrativeExamplesPart4(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1

class AdditionalRemarks(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1



class LinkReviewQuestions(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1



class FinalPage(Page):
    
    def is_displayed(self):
        return self.subsession.round_number == 1




class Welcome(Page):
    pass

class Question_1(Page):

    form_model = models.Player
    form_fields = [
        "gender"]

class Question_1_Answers(Page):
    pass


class Question_2(Page):
    
    form_model = models.Player
    form_fields = [
                    "age"]


class Question_2_Answers(Page):
    pass


class Question_3(Page):
    
    form_model = models.Player
    form_fields = [
                   "education_level"]


class Question_3_Answers(Page):
    pass



class Question_4(Page):
    
    form_model = models.Player
    form_fields = [
                   "marital_status"]


class Question_4_Answers(Page):
    pass



class Question_5(Page):
    
    form_model = models.Player
    form_fields = [
                   "employment_status"]


class Question_5_Answers(Page):
    pass


class Question_6(Page):
    
    form_model = models.Player
    form_fields = [
                   "student_status"]


class Question_6_Answers(Page):
    pass

class Question_7(Page):
    
    form_model = models.Player
    form_fields = [
                   "example1"]


class Question_7_Answers(Page):
    pass


class Question_8(Page):
    
    form_model = models.Player
    form_fields = [
                   "example2"]


class Question_8_Answers(Page):
    pass


class Link(Page):
    pass 

page_sequence = [ FirstPage,
                 SecondPage,
                 Introduction_1,
                 Introduction_2,
                 AssignmentRulesAndProfitCalculations,
                 IllustrativeExamplesPart1Section1,
                 IllustrativeExamplesPart1Section2,
                 IllustrativeExamplesPart1Section3,
                 IllustrativeExamplesPart1Section4,
                 IllustrativeExamplesPart2,
                 IllustrativeExamplesPart3,
                 IllustrativeExamplesPart4,
                 AdditionalRemarks,
                 LinkReviewQuestions,
                 Welcome,
                 Question_1,
                 Question_1_Answers,
                 Question_2,
                 Question_2_Answers,
                 Question_3,
                 Question_3_Answers,
                 Question_4,
                 Question_4_Answers,
                 Question_5,
                 Question_5_Answers,
                 Question_6,
                 Question_6_Answers,
                 Question_7,
                 Question_7_Answers,
                 Question_8,
                 Question_8_Answers,
                 Link,
                 FinalPage]

"""(Poorly) testing the app
"""
from django.test import TestCase

from factory import DjangoModelFactory

from .models import Question, Choice


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice


class QuestionTest(TestCase):
    def setUp(self):
        self.question = QuestionFactory(question_text="Question one ?")

    def test_initial_responses_count(self):
        self.assertEqual(self.question.responses_count, 0)

    def test_with_choices(self):
        # Initial choices first
        choice1 = ChoiceFactory(question=self.question, choice_text="Choice1")
        choice2 = ChoiceFactory(question=self.question, choice_text="Choice2")
        choice3 = ChoiceFactory(question=self.question, choice_text="Choice3")
        self.assertEqual(self.question.responses_count, 0)

        choice1.votes = 10
        choice1.save()
        choice2.votes = 11
        choice2.save()
        choice3.votes = 12
        choice3.save()
        self.assertEqual(self.question.responses_count, 33)

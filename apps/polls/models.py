"""Persistent data models"""

import datetime
from functools import lru_cache

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A question for a poll, may have many :model:`polls.Choice`
    """
    question_text = models.CharField(max_length=200, help_text="Question text")
    pub_date = models.DateTimeField('date published', default=timezone.now, help_text="Publication date")

    @property
    def responses_count(self):
        """Total number of responses (all choices)"""
        return sum((choice.votes for choice in self.choice_set.iterator()))

    def __str__(self):
        return "{0.id}: {0.question_text}".format(self)

    class Meta:
        verbose_name = "Question: A question of a poll"
        verbose_name_plural = "Questions of polls"


class Choice(models.Model):
    """A possible answer for a :model:`Question`
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, help_text="Related question")
    choice_text = models.CharField(max_length=200, help_text="Choice text")
    votes = models.IntegerField(default=0, help_text="Votes count for this choice")

    @property
    def votes_percent(self):
        """Votes in percent among all choices of same question
        """
        return 100.0 * self.votes / self.question.responses_count

    def __str__(self):
        return "{0.id}: {0.choice_text}".format(self)

    class Meta:
        verbose_name = "Choice: Answer for a question"
        verbose_name_plural = "Answers for questions"

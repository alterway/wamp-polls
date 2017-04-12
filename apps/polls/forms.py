"""Forms for this app"""

from django import forms
from django.shortcuts import get_object_or_404

from . import models

CHOICES = [
    ('1', "One"),
    ('2', "Two"),
    ('3', "Three")
]


class VoteForm(forms.Form):
    """Form with radios vor various question choices
    """
    vote = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    @classmethod
    def make_vote_form(cls, question):
        """Makes dynamically a new form class based on this one because form fields
        don't support context based properties
        """
        field_choices = [(choice.pk, choice.choice_text) for choice in question.choice_set.all()]
        vote_field = forms.ChoiceField(choices=field_choices, widget=forms.RadioSelect)
        return type('VoteForm', (VoteForm,), {'vote': vote_field})

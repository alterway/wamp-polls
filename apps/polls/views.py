"""Views for the app"""

from functools import lru_cache
import requests

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .forms import VoteForm
from .models import Choice, Question


class IndexView(ListView):
    """Batched view of questions (latest first)
    """
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'
    paginate_by = 20
    ordering = '-pub_date'


class VoteView(FormView):
    """Vote form and results view
    """
    form_class = VoteForm
    template_name = 'polls/vote.html'
    success_url = '.'

    @lru_cache()
    def _get_question(self, question_id):
        """Gets and cache the question for a PK
        """
        return get_object_or_404(Question, pk=question_id)

    def get_form_class(self):
        question_id = int(self.kwargs['question_id'])
        question = self._get_question(question_id)
        return VoteForm.make_vote_form(question)

    def form_valid(self, form):
        """Handling successful form submit
        """
        # We save the new result
        choice_id = int(form.data['vote'])
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.votes += 1
        choice.save()

        # We publish the new result to subscribers
        question_id = int(self.kwargs['question_id'])
        question = self._get_question(question_id)
        message = {
            'question_id': question_id,
            'total_votes': question.responses_count,
            'choices': [
                {'id': choice.id,
                 'votes': choice.votes,
                 'percent': choice.votes_percent}
                for choice in question.choice_set.iterator()
            ]
        }
        response = wamp_publish(message)

        # Notifying the publication success (or error) in the UI
        if isinstance(response, requests.exceptions.ConnectionError):
            err_msg = "Could not connect with the WAMP router bridge {}".format(settings.MY_WAMP_HTTP_GATEWAY)
        elif not response.ok:
            err_msg = "Notification could not be issued ({}: {})".format(response.status_code, response.reason)
        else:
            err_msg = False
        if err_msg:
            messages.error(self.request, err_msg)
        else:
            messages.info(self.request, "Your vote is spreading to the world!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Extra data for template
        """
        question_id = int(self.kwargs['question_id'])
        question = self._get_question(question_id)
        kwargs.setdefault('question', question)
        choices = question.choice_set.all()
        kwargs.setdefault('choices', choices)
        return super().get_context_data(**kwargs)


def wamp_publish(message):
    """Making a WAMP PUB throug the http bridge.
    http://crossbar.io/docs/HTTP-Bridge-Publisher/
    """
    payload = {
        'topic': 'question.update',
        'args': [message]
    }
    try:
        response = requests.post(settings.MY_WAMP_HTTP_GATEWAY, json=payload)
    except requests.ConnectionError as exc:
        # B plan when running Django debug server or unit tests without Crossbar
        response = exc
    return response

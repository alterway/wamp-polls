from django.core.management.base import BaseCommand, CommandError

from apps.polls.tests import QuestionFactory, ChoiceFactory
from apps.polls.models import Question, Choice


class Command(BaseCommand):
    help = "Create additional questions"

    def add_arguments(self, parser):
        parser.add_argument('questions_count', nargs='?', default=1, type=int,
                            help="Add questions_count questions")
        parser.add_argument('--choices-count', dest='choices_count', default=3, type=int,
                            metavar='COUNT', help="Choices per question (default 3)")

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(self.help))
        questions_count = options.get('questions_count', 1)
        choices_count = options.get('choices_count', 3)
        msg = "Creating {0[questions_count]} question(s) with {0[choices_count]} choice(s) each."
        self.stdout.write(self.style.NOTICE(msg.format(locals())))
        for i, _ in enumerate(range(questions_count), 1):
            question_text = "Question #{0[i]}?".format(locals())
            new_question = Question(question_text=question_text)
            new_question.save()
            for j, _ in enumerate(range(choices_count), 1):
                choice_text = "Choice #{0[j]} of question #{0[i]}.".format(locals())
                new_choice = Choice(question=new_question, choice_text=choice_text, votes=j)
                new_choice.save()
        self.stdout.write(self.style.SUCCESS("Done!"))

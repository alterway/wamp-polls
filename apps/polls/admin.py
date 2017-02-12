from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    """Managing question and associated choices in the same form
    """
    list_display = ('question_text', 'pub_date')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields':('pub_date',), 'classes': 'collapse'})
    )
    inlines = (ChoiceInline,)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

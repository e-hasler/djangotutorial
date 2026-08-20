"""
polls/admins.py

Register your models here.
"""

from django.contrib import admin
from .models import Question, Choice

# Admin classes
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # choose order of fields to display with fields = ["field", ...]
    # and split in sets using fieldsets = [("DesiredFieldName", {"fields": ["field"]}), ...]
    fieldsets = [
        ("Da question", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]

# Register all models admins want to control
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

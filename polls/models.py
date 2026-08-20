"""
A model is like a type of elements on a page.
"""

import datetime

from django.db import models
from django.utils import timezone

# My models

# To create instances of models run "python manage.py shell"
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # Display question_text when checking Question.objects.all()
    def __str__(self):
        return self.question_text

    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days = 1)
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
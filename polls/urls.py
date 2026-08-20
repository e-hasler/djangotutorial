"""
djangotutorial/polls/urls.py 

We associate each view (i.e. page) with a URL
"""

from django.urls import path
from . import views

app_name = "polls" # Add if several apps in the project
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
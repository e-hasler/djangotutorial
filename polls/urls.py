"""
We associate each view (i.e. page) with a URL
"""

from django.urls import path
from . import views

app_name = "polls" # Add if several apps in the project
urlpatterns = [
    path("", views.index, name="index"),
    path("specifics/<int:question_id>", views.detail, name="detail"),
    path("<int:question_id>/result", views.results, name="results"), 
    # Why only views.results since it is associated to a question (that is not given here)?
    # How does it know the results of which question to display?
    path("<int:question_id>/vote", views.vote, name = "vote"),
    # Same question here
]
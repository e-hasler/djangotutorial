"""
The views are the different types of pages
"""

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader


from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context) # We provide the template path and the context

    """
    return render(request, "polls/index.html", context)

    is a shortcut for 

    template = loader.get_template("polls/index.html")
    return HttpResponse(template.render(context, request))
    """

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    return HttpResponse("You are looking at the results of question %s" % question_id)

def vote(request, question_id):
    return HttpResponse("You are on the voting page of question %s" % question_id)
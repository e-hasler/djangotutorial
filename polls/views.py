"""
views.py
The views are the different types of pages
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Choice, Question

class LoginView(generic.TemplateView):
    template_name = "polls/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) # checks that the user can indeed login
        # it checks that the username is in my User table
        # it compares the hash password against the hash stored
        # if it matches, it returns a User object
        if user is not None:
            login(request, user) # writes the user's ID into the session, and Django sets a sessionid cookie in the browser's response
            return redirect("polls:index") # if yes it redirects to the index page
        else:
            return self.render_to_response({"error": "Invalid credentials"})


# class LogoutView(generic.TemplateView):
#     template_name = "polls/logout.html"
#     def post(self, request, *args, **kwargs):
#         logout(request) # logout flushes the session 
#         return self.render(request, self.template_name, {"message": "You have been logged out."})
    
    
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions excluding those set to publish in the future"""
        questions = Question.objects.filter(pub_date__lte=timezone.now())
        return questions.order_by("-pub_date")[:5]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"

@login_required(login_url="polls:login")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form 
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def logout_view(request):
    logout(request)
    return render(request, "polls/logout.html")

# function to create a new account
def create_account(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "polls/create_account.html", {"error": "Username already exists"})
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("polls:index")
    else:
        return render(request, "polls/create_account.html")
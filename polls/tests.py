import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(days=1) + datetime.timedelta(seconds=1)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

# Tests with new questions

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):


    # Always login first, runs before each test
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.client.force_login(self.user)

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        # Check no question behavior
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

# Tests that the detail view of a question with a pub_date in the future returns a 404 not found

class QuestionDetailViewTests(TestCase):

    # Always login first, runs before each test
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.client.force_login(self.user)
        
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# User authentification

"""
Do this once my website supports account creation

def create_user():

def test_user_access()
    #Tests that an existing user can access the polls/ app

def test_incognito_access():
    #Tests that we can't access views without being authentificated first

"""

# Login test

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")

    def test_login_with_correct_credentials_redirects(self):
        response = self.client.post(reverse("polls:login"), {
            "username": "alice",
            "password": "secret123",
        })
        self.assertRedirects(response, reverse("polls:index"))

    def test_login_with_wrong_password_shows_error(self):
        response = self.client.post(reverse("polls:login"), {
            "username": "alice",
            "password": "wrongpassword",
        })
        self.assertContains(response, "Invalid credentials")

# Logout test

class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("polls:logout"))
        # check that the user is logged out by checking the session
        self.assertNotIn("_auth_user_id", self.client.session)


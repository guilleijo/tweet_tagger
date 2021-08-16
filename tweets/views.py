import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from tweets.forms import ClassificationForm
from tweets.models import Classification, Tweet


class HomeView(LoginRequiredMixin, View):
    login_url = "/admin/login/"
    template_name = "home.html"
    htmx_template_name = "htmx/tweet.html"

    def _get_tweet(self, request: HttpRequest, template_name):
        try:
            tweets = Tweet.objects.exclude(classifications__user=request.user)
            random_tweet = random.choice(list(tweets))
        except Exception:
            return render(request, template_name, {"no_tweets": True})

        return render(request, template_name, {"tweet": random_tweet})

    def get(self, request: HttpRequest, *args, **kwargs):
        return self._get_tweet(request, self.template_name)

    def post(self, request: HttpRequest, *args, **kwargs):
        user = request.user

        form = ClassificationForm(request.POST)
        if not form.is_valid():
            return redirect("/")

        tweet_id = form.cleaned_data.get("tweet_id")
        value = form.cleaned_data.get("value")

        bool_value = {
            "Yes": True,
            "No": False,
            "Skip": None,
        }.get(value, True)
        tweet = get_object_or_404(Tweet, id=tweet_id)

        if bool_value is not None:
            Classification.objects.create(
                user=user,
                is_seguridad=bool_value,
                tweet=tweet,
            )

        return self._get_tweet(request, self.htmx_template_name)

import random

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from tweets.models import Tweet
from tweets.forms import ClassificationForm


from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    login_url = "/admin/login/"
    template_name = "home.html"
    htmx_template_name = "htmx/tweet.html"

    def _get_tweet(self, request, template_name):
        try:
            tweets = Tweet.objects.filter(is_seguridad__isnull=True)
            random_tweet = random.choice(list(tweets))
        except Exception:
            return render(request, template_name, {"no_tweets": True})

        return render(request, template_name, {"tweet": random_tweet})

    def get(self, request, *args, **kwargs):
        return self._get_tweet(request, self.template_name)

    def post(self, request, *args, **kwargs):
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

        tweet.is_seguridad = bool_value
        tweet.save()

        return self._get_tweet(request, self.htmx_template_name)

import random

from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from tweets.models import Tweet
from tweets.forms import ClassificationForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        try:
            tweets = Tweet.objects.filter(is_seguridad__isnull=True)
            random_tweet = random.choice(list(tweets))
        except Exception:
            return render(request, self.template_name, {"no_tweets": True})

        return render(request, self.template_name, {"tweet": random_tweet})

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
        }.get(value, None)
        tweet = get_object_or_404(Tweet, id=tweet_id)

        tweet.is_seguridad = bool_value
        tweet.save()

        return redirect("/")

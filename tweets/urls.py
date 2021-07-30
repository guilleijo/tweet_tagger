from django.urls import path

from .views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
]


# from django.urls import path

# from .views import index_view, tweet_view


# urlpatterns = [
#     path("", index_view, name="home_page"),
#     path("tweet/", tweet_view, name="tweet"),
# ]

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tweet(models.Model):
    text = models.TextField(blank=True)
    tweet_url = models.URLField(max_length=255)
    account = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.account} - {self.text[:100]}..."


class Classification(models.Model):
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="classifications"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="classifications"
    )
    is_seguridad = models.BooleanField(null=True)

from django.db import models


class Tweet(models.Model):
    text = models.TextField(blank=True)
    tweet_url = models.URLField(max_length=255)
    is_seguridad = models.BooleanField(null=True)
    account = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.account} - {self.is_seguridad} - {self.text[:100]}..."

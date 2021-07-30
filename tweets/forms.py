from django import forms


STATUS_CHOICES = (
    ("Yes", "Yes"),
    ("No", "No"),
    ("Skip", "Skip"),
)


class ClassificationForm(forms.Form):
    value = forms.ChoiceField(required=True, choices=STATUS_CHOICES)
    tweet_id = forms.CharField(required=True, max_length=10)

from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from tweets.models import Tweet


class TweetResource(resources.ModelResource):
    class Meta:
        model = Tweet


@admin.register(Tweet)
class TweetAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "text",
        "account",
        "is_seguridad",
    )

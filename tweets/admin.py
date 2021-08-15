from django.contrib import admin
from django.db.models import Q, Count

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from tweets.models import Classification, Tweet


class TweetResource(resources.ModelResource):
    class Meta:
        model = Tweet


@admin.register(Tweet)
class TweetAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "text",
        "account",
        "si_seguridad",
        "no_seguridad",
    )

    fields = (
        "id",
        "text",
        "account",
        "si_seguridad",
        "no_seguridad",
    )
    readonly_fields = ("id", "si_seguridad", "no_seguridad")
    search_fields = ("id", "text", "account")

    def si_seguridad(self, obj):
        return obj.positive_tag

    def no_seguridad(self, obj):
        return obj.negative_tag

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("classifications").annotate(
            positive_tag=Count("id", filter=Q(classifications__is_seguridad=True)),
            negative_tag=Count("id", filter=Q(classifications__is_seguridad=False)),
        )
        return qs


@admin.register(Classification)
class ClassificationAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "user",
        "is_seguridad",
        "tweet",
    )

    list_select_related = ["tweet", "user"]
    autocomplete_fields = ["tweet", "user"]

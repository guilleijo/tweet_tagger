from django.contrib import admin
from django.db.models import Count, Q
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
        return obj._positive_classification

    def no_seguridad(self, obj):
        return obj._negative_classification

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("classifications").annotate(
            _positive_classification=Count(
                "id", filter=Q(classifications__is_seguridad=True)
            ),
            _negative_classification=Count(
                "id", filter=Q(classifications__is_seguridad=False)
            ),
        )
        return qs

    si_seguridad.admin_order_field = "_positive_classification"
    no_seguridad.admin_order_field = "_negative_classification"


@admin.register(Classification)
class ClassificationAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "user",
        "is_seguridad",
        "tweet",
    )

    list_select_related = ("tweet", "user")
    autocomplete_fields = ("tweet", "user")
    search_fields = (
        "id",
        "user__id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

from django.contrib import admin
from django.db.models import Count, Q
from django.contrib.postgres.aggregates import ArrayAgg

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from tweets.models import Classification, Tweet

site_name = "tweet tagger"
admin.site.site_header = site_name
admin.site.site_title = site_name
admin.site.index_title = "Admin"

class ClassificationInline(admin.StackedInline):
    model = Classification
    extra = 0
    show_change_link = True
    autocomplete_fields = ["user"]
    readonly_fields = ["user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("user")
        return qs


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
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


class TweetImportResource(resources.ModelResource):
    """Ignore classifications/classifiers on import"""

    class Meta:
        model = Tweet


class TweetResource(resources.ModelResource):
    positive_classification = Field(attribute="_positive_classification")
    negative_classification = Field(attribute="_negative_classification")

    positive_classifiers = Field(attribute="_positive_classifiers")
    negative_classifiers = Field(attribute="_negative_classifiers")

    class Meta:
        model = Tweet


@admin.register(Tweet)
class TweetAdmin(ImportExportModelAdmin):
    resource_class = TweetResource

    list_display = (
        "id",
        "text",
        "account",
        "si_seguridad",
        "no_seguridad",
        "positive_classifiers",
        "negative_classifiers",
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
    inlines = (ClassificationInline,)

    def si_seguridad(self, obj):
        return obj._positive_classification

    def no_seguridad(self, obj):
        return obj._negative_classification

    def positive_classifiers(self, obj):
        return obj._positive_classifiers

    def negative_classifiers(self, obj):
        return obj._negative_classifiers

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("classifications", "classifications__user").annotate(
            _positive_classification=Count(
                "id", filter=Q(classifications__is_seguridad=True)
            ),
            _negative_classification=Count(
                "id", filter=Q(classifications__is_seguridad=False)
            ),
            _positive_classifiers=ArrayAgg(
                "classifications__user__username",
                filter=Q(classifications__is_seguridad=True),
            ),
            _negative_classifiers=ArrayAgg(
                "classifications__user__username",
                filter=Q(classifications__is_seguridad=False),
            ),
        )
        return qs

    def get_import_resource_class(self):
        return TweetImportResource

    si_seguridad.admin_order_field = "_positive_classification"
    no_seguridad.admin_order_field = "_negative_classification"

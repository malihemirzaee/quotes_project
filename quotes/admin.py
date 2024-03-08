from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(ImportExportModelAdmin):
    fields = (
        "_id",
        "author",
        "content",
        "tags",
        "authorSlug",
        "length",
        "dateAdded",
        "dateModified",
    )
    list_display = ("_id", "author")
    readonly_fields = ("_id",)
    search_fields = ("_id", "author", "tags")
    list_filter = ("author",)

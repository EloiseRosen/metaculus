from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [AutocompleteFilterFactory("Author", "author")]
    autocomplete_fields = [
        "author",
        "approved_by",
        "question",
        "projects",
        "conditional",
        "group_of_questions",
    ]
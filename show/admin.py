from django.contrib import admin

from show.models import Show, Author, Episode


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'is_include_explicit_language')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'show')

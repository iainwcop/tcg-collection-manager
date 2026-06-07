from django.contrib import admin

from .models import CardDefinition, CardSet, Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "game", "release_date")
    list_filter = ("game",)
    search_fields = ("name", "code")


@admin.register(CardDefinition)
class CardDefinitionAdmin(admin.ModelAdmin):
    list_display = ("name", "set", "collector_number", "rarity")
    list_filter = ("set__game", "set", "rarity")
    search_fields = ("name", "collector_number")

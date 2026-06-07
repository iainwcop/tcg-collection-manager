from rest_framework import serializers

from .models import CardDefinition, CardSet, Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id", "name", "slug")


class CardSetSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = CardSet
        fields = ("id", "game", "name", "code", "release_date")


class CardDefinitionSerializer(serializers.ModelSerializer):
    set = CardSetSerializer(read_only=True)

    class Meta:
        model = CardDefinition
        fields = (
            "id",
            "set",
            "name",
            "collector_number",
            "rarity",
            "image_url",
            "metadata",
        )

from rest_framework import serializers

from apps.catalog.models import CardDefinition
from apps.catalog.serializers import CardDefinitionSerializer

from .models import CardInstance, Collection, Slot, StorageUnit


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ("id", "parent_slot", "label", "sort_order")
        read_only_fields = ("id",)


class StorageUnitSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta:
        model = StorageUnit
        fields = ("id", "type", "name", "config", "slots", "created_at")
        read_only_fields = ("id", "created_at")


class CardInstanceSerializer(serializers.ModelSerializer):
    card_definition = CardDefinitionSerializer(read_only=True)
    card_definition_id = serializers.PrimaryKeyRelatedField(
        queryset=CardDefinition.objects.all(),
        source="card_definition",
        write_only=True,
    )

    class Meta:
        model = CardInstance
        fields = (
            "id",
            "card_definition",
            "card_definition_id",
            "slot",
            "quantity",
            "condition",
            "notes",
            "tags",
            "acquired_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

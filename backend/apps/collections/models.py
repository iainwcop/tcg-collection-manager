from django.conf import settings
from django.db import models

from apps.catalog.models import CardDefinition


class Collection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collections",
    )
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = [("user", "name")]

    def __str__(self):
        return self.name


class StorageUnit(models.Model):
    class UnitType(models.TextChoices):
        BINDER = "binder", "Binder"
        BOX = "box", "Box"
        CUSTOM = "custom", "Custom"

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="storage_units",
    )
    type = models.CharField(max_length=20, choices=UnitType.choices)
    name = models.CharField(max_length=200)
    config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Slot(models.Model):
    storage_unit = models.ForeignKey(
        StorageUnit,
        on_delete=models.CASCADE,
        related_name="slots",
    )
    parent_slot = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    label = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self):
        return f"{self.storage_unit.name} / {self.label}"


class CardInstance(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="card_instances",
    )
    card_definition = models.ForeignKey(
        CardDefinition,
        on_delete=models.PROTECT,
        related_name="instances",
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="card_instances",
    )
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    acquired_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.card_definition.name} x{self.quantity}"

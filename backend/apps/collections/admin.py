from django.contrib import admin

from .models import CardInstance, Collection, Slot, StorageUnit


class StorageUnitInline(admin.TabularInline):
    model = StorageUnit
    extra = 0


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "user__username", "user__email")
    inlines = [StorageUnitInline]


@admin.register(StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "collection")
    list_filter = ("type",)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("label", "storage_unit", "sort_order")


@admin.register(CardInstance)
class CardInstanceAdmin(admin.ModelAdmin):
    list_display = ("card_definition", "collection", "quantity", "condition", "slot")
    list_filter = ("collection", "condition")
    search_fields = ("card_definition__name", "notes")

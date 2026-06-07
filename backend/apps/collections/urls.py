from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CardInstanceViewSet, CollectionViewSet, StorageUnitViewSet

router = DefaultRouter()
router.register("collections", CollectionViewSet, basename="collection")

collection_list = CollectionViewSet.as_view({"get": "list", "post": "create"})
collection_detail = CollectionViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
storage_unit_list = StorageUnitViewSet.as_view({"get": "list", "post": "create"})
storage_unit_detail = StorageUnitViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
card_instance_list = CardInstanceViewSet.as_view({"get": "list", "post": "create"})
card_instance_detail = CardInstanceViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("collections/", collection_list, name="collection-list"),
    path("collections/<int:pk>/", collection_detail, name="collection-detail"),
    path(
        "collections/<int:collection_pk>/storage-units/",
        storage_unit_list,
        name="collection-storage-unit-list",
    ),
    path(
        "collections/<int:collection_pk>/storage-units/<int:pk>/",
        storage_unit_detail,
        name="collection-storage-unit-detail",
    ),
    path(
        "collections/<int:collection_pk>/instances/",
        card_instance_list,
        name="collection-instance-list",
    ),
    path(
        "collections/<int:collection_pk>/instances/<int:pk>/",
        card_instance_detail,
        name="collection-instance-detail",
    ),
]

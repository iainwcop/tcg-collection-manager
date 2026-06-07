from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import CardInstance, Collection, StorageUnit
from .serializers import CardInstanceSerializer, CollectionSerializer, StorageUnitSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StorageUnitViewSet(viewsets.ModelViewSet):
    serializer_class = StorageUnitSerializer

    def get_queryset(self):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs["collection_pk"],
            user=self.request.user,
        )
        return StorageUnit.objects.filter(collection=collection).prefetch_related("slots")

    def perform_create(self, serializer):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs["collection_pk"],
            user=self.request.user,
        )
        serializer.save(collection=collection)


class CardInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = CardInstanceSerializer

    def get_queryset(self):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs["collection_pk"],
            user=self.request.user,
        )
        return CardInstance.objects.filter(collection=collection).select_related(
            "card_definition__set__game",
            "slot",
        )

    def perform_create(self, serializer):
        collection = get_object_or_404(
            Collection,
            pk=self.kwargs["collection_pk"],
            user=self.request.user,
        )
        serializer.save(collection=collection)

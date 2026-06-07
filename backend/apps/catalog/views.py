from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import CardDefinition, CardSet, Game
from .serializers import CardDefinitionSerializer, CardSetSerializer, GameSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class CardSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CardSet.objects.select_related("game").all()
    serializer_class = CardSetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["game"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "release_date"]


class CardDefinitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CardDefinition.objects.select_related("set__game").all()
    serializer_class = CardDefinitionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["set", "set__game", "rarity"]
    search_fields = ["name", "collector_number"]
    ordering_fields = ["name", "collector_number"]

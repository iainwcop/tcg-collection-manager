from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CardDefinitionViewSet, CardSetViewSet, GameViewSet

router = DefaultRouter()
router.register("games", GameViewSet, basename="game")
router.register("sets", CardSetViewSet, basename="card-set")
router.register("cards", CardDefinitionViewSet, basename="card-definition")

urlpatterns = [
    path("", include(router.urls)),
]

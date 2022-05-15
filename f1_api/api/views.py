from rest_framework import viewsets
from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
from api.mixins import ReadOnlyModelViewsetCacheMixin

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class DriversViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer

    filterset_fields = ["surname", "forename", "nationality"]
    search_fields = ["surname", "forename"]
    ordering_fields = ["name", "surname", ""]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

class ConstructorsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

class RacesViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class SeasonsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
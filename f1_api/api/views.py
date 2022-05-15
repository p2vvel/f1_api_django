from rest_framework import viewsets
from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
from api.mixins import ReadOnlyModelViewsetCacheMixin


class DriversViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer

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
from django.views import View
from rest_framework import viewsets

from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
# from api.throttling import ViewThrottle


class DriversViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


class ConstructorsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

class RacesViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class SeasonsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
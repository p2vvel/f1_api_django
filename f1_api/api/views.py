from django.views import View
from rest_framework import viewsets

from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
from api.throttling import ViewThrottle


class DriversViewset(viewsets.ModelViewSet, ViewThrottle):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


class ConstructorsViewset(viewsets.ModelViewSet, ViewThrottle):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(viewsets.ModelViewSet, ViewThrottle):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

class RacesViewset(viewsets.ModelViewSet, ViewThrottle):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class SeasonsViewset(viewsets.ModelViewSet, ViewThrottle):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
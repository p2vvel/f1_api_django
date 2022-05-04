from rest_framework import viewsets

from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer


class DriversViewset(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


class ConstructorsViewset(viewsets.ModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(viewsets.ModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

class RacesViewset(viewsets.ModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class SeasonsViewset(viewsets.ModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
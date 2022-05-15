from django.views import View
from rest_framework import viewsets

from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
# from api.throttling import ViewThrottle
from rest_framework.response import Response

from django.core.cache import cache
from api.mixins import ReadOnlyThrottledMixin


class DriversViewset(ReadOnlyThrottledMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer

class ConstructorsViewset(ReadOnlyThrottledMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(ReadOnlyThrottledMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

class RacesViewset(ReadOnlyThrottledMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer

class SeasonsViewset(ReadOnlyThrottledMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
from rest_framework import viewsets
from api.models import Circuits, Drivers, Constructors, Races, Seasons
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer, RaceSerializer, SeasonSerializer
from api.mixins import ReadOnlyModelViewsetCacheMixin

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class DriversViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    basic_fields = ["surname", "forename", "nationality", "code", "number", "dob"]
    filterset_fields = basic_fields 
    search_fields = basic_fields
    ordering_fields = basic_fields


class ConstructorsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    basic_fields = ["name", "nationality"]
    filterset_fields = basic_fields 
    search_fields = basic_fields
    ordering_fields = basic_fields


class CircuitsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    basic_fields = ["name", "location", "country", "lat", "lng", "alt"]
    filterset_fields = basic_fields 
    search_fields = basic_fields
    ordering_fields = basic_fields


class RacesViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Races.objects.all()
    serializer_class = RaceSerializer
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    basic_fields = ["name", "year", "round", "date"]
    filterset_fields = basic_fields 
    search_fields = basic_fields
    ordering_fields = basic_fields


class SeasonsViewset(ReadOnlyModelViewsetCacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    basic_fields = ["year"]
    filterset_fields = basic_fields 
    search_fields = basic_fields
    ordering_fields = basic_fields
from django import views
from django.shortcuts import render
from rest_framework import viewsets

from api.models import Circuits, Drivers, Constructors
from api.serializers import DriverSerializer, ConstructorSerializer, CircuitSerializer
# Create your views here.


class DriversViewset(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


class ConstructorsViewset(viewsets.ModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer

class CircuitsViewset(viewsets.ModelViewSet):
    queryset = Circuits.objects.all()
    serializer_class = CircuitSerializer

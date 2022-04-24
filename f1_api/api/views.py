from django import views
from django.shortcuts import render
from rest_framework import viewsets

from api.models import Drivers, Constructors
from api.serializers import DriverSerializer, ConstructorSerializer
# Create your views here.


class DriversViewset(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


class ConstructorsViewset(viewsets.ModelViewSet):
    queryset = Constructors.objects.all()
    serializer_class = ConstructorSerializer


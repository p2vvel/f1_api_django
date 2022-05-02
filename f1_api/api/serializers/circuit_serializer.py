from rest_framework import serializers
from api.models import Circuits



class CircuitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Circuits
        fields = ["name", "location", "country", "lat", "lng", "alt", "url"]
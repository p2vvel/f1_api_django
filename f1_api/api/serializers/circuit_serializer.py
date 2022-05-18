from rest_framework import serializers
from api.models import Circuits, Races
from rest_framework.reverse import reverse



class CircuitSerializer(serializers.ModelSerializer):
    races = serializers.SerializerMethodField(method_name="get_races")


    def get_races(self, instance: Circuits) -> dict[int, list]:
        """
        Get list of races organized on the circuit

        Args:
            instance (Circuits): circuit object

        Returns:
            list[str]: list of urls to races organized on the track
        """
        races = Races.objects.filter(circuit=instance).order_by("year", "round")    # querying for races on the track
        years = {r.year for r in races}     # set of seasons with races on the track
        result = {y:[] for y in years}      # dict in format {year:[list, of, races]}
        for i, r in enumerate(races):
            year = r.year
            url = reverse("race-detail", args=(r.year, r.round))
            url = ""
            result[year].append(url)
        return result


    class Meta:
        model = Circuits
        fields = ["name", "location", "country", "lat", "lng", "alt", "url", "races"]
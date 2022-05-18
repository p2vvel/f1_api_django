from cgitb import lookup
from rest_framework import serializers
from api.models import ConstructorResults, Races, Results
from rest_framework.reverse import reverse



class RaceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name="get_url")
    driver_results = serializers.SerializerMethodField(method_name="get_drivers_results")
    constructors_results = serializers.SerializerMethodField(method_name="get_constructors_results")
    # circuit = serializers.HyperlinkedRelatedField(view_name="circuit-detail", lookup_field="pk", read_only=True)
    circuit = serializers.SerializerMethodField(method_name="get_circuit")

    def get_drivers_results(self, instance: Races) -> list[str]:
        """
        Get list of drivers taking part in race, ordered by position on the finish line

        Args:
            instance (Races): race object

        Returns:
            list[str]: list of urls to drivers taking part in race, ordered by position on the finish line
        """
        try:
            results = Results.objects.filter(race=instance).order_by("positionorder")
            drivers = [r.driver.driverref for r in results]
            drivers_urls = [reverse("driver-detail", args=(d.pk,)) for d in drivers]
            return drivers_urls
        except:
            return []
    

    def get_constructors_results(self, instance: Races) -> list[str]:
        """
        Get list of constructors taking part in the race, ordered by points scored

        Args:
            instance (Races): race object

        Returns:
            list[str]: list of urls to constructors taking part in the race, ordered by points scored
        """
        try:
            results = ConstructorResults.objects.filter(race=instance).order_by("-points")
            constructors = [r.constructor for r in results]
            constructors_urls = [reverse("constructor-detail", args=(c.constructorref,)) for c in constructors]
            return constructors_urls
        except:
            return []

    def get_circuit(self, instance: Races) -> str:
        """Return url to circuit that the race was organized on 

        Args:
            instance (Race): race object

        Returns:
            url: URL to circuit data
        """
        circuitref = instance.circuit.circuitref
        return reverse("circuit-detail", args=(circuitref,))
    

    def get_url(self, instance: Races) -> str:
        """Return URL to the race endpoint

        Args:
            instance (Races): race object

        Returns:
            str: URL to race
        """
        return reverse("race-detail", args=(instance.year, instance.round))

    class Meta:
        model = Races
        fields = ["url", "name", "year", "round", "date", "circuit", "url", "driver_results", "constructors_results"]

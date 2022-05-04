from rest_framework import serializers
from api.models import ConstructorResults, Races, Results
from rest_framework.reverse import reverse


class RaceSerializer(serializers.ModelSerializer):
    driver_results = serializers.SerializerMethodField(method_name="get_drivers_results")
    constructors_results = serializers.SerializerMethodField(method_name="get_constructors_results")


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

            drivers = [r.driver for r in results]
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
            constructors_urls = [reverse("constructor-detail", args=(c.pk,)) for c in constructors]
            return constructors_urls
        except:
            return []

    

    class Meta:
        model = Races
        fields = ["name", "year", "round", "date", "circuit", "url", "driver_results", "constructors_results"]

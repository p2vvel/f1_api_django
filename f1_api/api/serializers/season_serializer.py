from copyreg import constructor
from rest_framework import serializers
from api.models import ConstructorStandings, DriverStandings, Races, Seasons, Results
from rest_framework.reverse import reverse
from django.db.models import Max



class SeasonSerializer(serializers.ModelSerializer):
    races = serializers.SerializerMethodField(method_name="get_races")
    drivers = serializers.SerializerMethodField(method_name="get_drivers")
    constructors = serializers.SerializerMethodField(method_name="get_constructors")


    def get_races(self, instance: Seasons) -> list[str]:
        """
        Get list of races in the season

        Args:
            instance (Seasons): season object

        Returns:
            list[str]: list of url to races
        """
        try:
            races = Races.objects.filter(year=instance.year).order_by("round")
            races_urls = [reverse("race-detail", args=(r.pk,)) for r in races]
            return races_urls
        except:
            return []


    def get_drivers(self, instance: Seasons) -> list[str]:
        """
        Get list of drivers in the season, ordered by positions in wdc

        Args:
            instance (Seasons): season object

        Returns:
            list[str]: list of urls to drivers racing during the season, ordered by the position in wdc
        """
        try:
            last_round_query = DriverStandings.objects.filter(race__year=instance.year).aggregate(Max("race__round"))
            last_round = last_round_query["race__round__max"]
            
            drivers_standings = DriverStandings.objects.filter(race__round=last_round, race__year=instance.year).order_by("position").values("driver__driverref")
            drivers_urls = [reverse("driver-detail", args=(d["driver__driverref"],)) for d in drivers_standings]
            return drivers_urls
        except Exception as e:
            print(e)
            return []


    def get_constructors(self, instance: Seasons) -> list[str]:
        """
        Get list of teams in the season, ordered by positions in wcc

        Args:
            instance (Seasons): season object

        Returns:
            list[str]: list of urls to constructors racing during the season, ordered by the position in the wcc
        """
        try:
            # The Constructors Championship was not awarded until 1958:
            if instance.year >= 1958:
                last_round_query = DriverStandings.objects.filter(race__year=instance.year).aggregate(Max("race__round"))
                last_round = last_round_query["race__round__max"]
                
                constructors_standings = ConstructorStandings.objects.filter(race__round=last_round, race__year=instance.year).order_by("position").values("constructor__pk")
                constructors_urls = [reverse("constructor-detail", args=(c["constructor__pk"],)) for c in constructors_standings]
                # constructors_urls = [Constructors.objects.get(pk=c["constructor__pk"]).name for c in constructors_standings]
                return constructors_urls
            else:
                # list constructors alphabetically
                teams_query = Results.objects.filter(race__year=1950).order_by("constructor__name").values("constructor", "constructor__name").distinct()
                teams_urls = [reverse("constructor-detail", args=(t.get("constructor"),)) for t in teams_query]
                return teams_urls
        except Exception as e:
            print(e)
            return []


    class Meta:
        model = Seasons
        fields = ["year", "url", "races", "drivers", "constructors"]

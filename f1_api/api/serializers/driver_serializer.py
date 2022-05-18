from cgitb import lookup
from typing import OrderedDict
from rest_framework import serializers
from api.models import Drivers
from django.db.models import Q, Max, Sum, Count
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.reverse import reverse
from api.models import DriverStandings
from api.utils import q_or



class DriverSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="driver-detail", lookup_field="driverref")
    poles = serializers.SerializerMethodField("get_poles")
    age = serializers.SerializerMethodField("get_current_age")
    wiki_url = serializers.URLField(source="url")


    def get_wins(self, driver: Drivers) -> int:
        """
        Get number of won races

        Args:
            driver (Drivers): driver object
        Returns:
            int: number won races
        """
        return self.podiums_data.get("1", 0)


    def get_podiums(self, driver: Drivers) -> int:
        """
        Get number of podiums

        Args:
            driver (Drivers): driver object
        Returns:
            int: number of races finished on podium 
        """
        return sum(self.podiums_data.values())


    def get_poles(self, driver: Drivers) -> int:
        """
        Get number of pole positionss

        Args:
            driver (Drivers): driver object

        Returns:
            int: amount of won pole positions
        """
        return driver.qualifying_set.filter(position=1).count()


    def get_current_age(self, driver: Drivers) -> int | None:
        """
        Return age of driver

        Args:
            driver (Drivers): driver object

        Returns:
            int: drivers current age 
        """
        if driver.dob:
            now = datetime.now()
            age = relativedelta(now, driver.dob)
            return age.years
        else:
            return None


    def get_teams_info(self, instance: Drivers) -> dict[int, list]:
        """
        Return dict containing lists of teams driver was racing for per season

        Args:
            instance (_type_): constructor object

        Returns:
            dict: dict containing lists of teams driver was racing for per season
        """
        query = instance.results_set.values_list("race__year", "constructor__constructorref").distinct()
        years_active = {year for year, constructor in query}        # years of activity in F1 for driver
        result = {year: [] for year in years_active}
        for year, constructor in query:
            constructor_url = reverse("constructor-detail", args=(constructor,))
            result[year].append(constructor_url)
        return result


    def get_wdc_info(self, instance: Drivers) -> list[int]:
        """
        Get list of championship winning seasons for the driver

        Args:
            instance (_type_): driver object

        Returns:
            list[int]: list of championship winning seasons
        """
        try:
            driver_wdc_position = DriverStandings.objects.filter(driver=instance, position=1).filter(self.condition).order_by("race__year").values("race__year")
            return [k["race__year"] for k in driver_wdc_position]
        except:
            return []   # return empty list if driver wasnt't classified at the end of the season (e.g. Markus Winkelhock)


    def get_points_info(self, instance: Drivers) -> int | None:
        """
        Return info about all points scored by driver during the career

        Args:
            instance (_type_): driver object

        Returns:
            int | None: amount of points scored by driver during the whole career
        """
        try:
            driver_results = DriverStandings.objects.filter(driver=instance).filter(self.condition).aggregate(Sum("points"))
            return driver_results["points__sum"]
        except:
            return None


    def to_representation(self, instance: Drivers) -> OrderedDict:
        """
        Add extra fields to serializer
        """
        representation =  super().to_representation(instance)       # default representation
        
        season_results = DriverStandings.objects.filter(driver=instance)\
                     .values("race__year").order_by("race__year").annotate(last_round=Max("race__round"))
        self.condition = q_or([Q(race__round=k["last_round"], race__year=k["race__year"]) for k in season_results])
        podiums_data = instance.results_set.filter(Q(position=1) | Q(position=2) | Q(position=3)).values("position").annotate(count=Count("position")).order_by("position")
        self.podiums_data = {k["position"]: k["count"] for k in podiums_data}

        representation["wins"] = self.get_wins(instance)
        representation["podiums"] = self.get_podiums(instance)
        representation["teams"] = self.get_teams_info(instance)        # add info to representation
        representation["wdc_seasons"] = self.get_wdc_info(instance)
        representation["points"] = self.get_points_info(instance)
        return representation


    class Meta:
        model = Drivers
        fields = ["url", "code", "number", "forename", "surname", "age", "dob", "nationality", "wiki_url", "poles"]
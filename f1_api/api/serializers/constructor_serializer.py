from typing import OrderedDict
from rest_framework import serializers
from api.models import Constructors
from django.db.models import Q, Max, Sum
from rest_framework.reverse import reverse
from api.models import ConstructorStandings
from django.db.models import Count
from api.utils import q_or



class ConstructorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="constructor-detail", lookup_field="constructorref")
    poles = serializers.SerializerMethodField()


    def get_wins(self, constructor: Constructors) -> int:
        """
        Get number of won races

        Args:
            constructor (Constructors): constructor object

        Returns:
            int: number of won races
        """
        return self.podiums_data.get(1, 0)


    def get_podiums(self, constructor: Constructors) -> int:
        """
        Get number of podiums

        Args:
            constructor (Constructors): constructor object

        Returns:
            int: number of races finished on podium
        """
        return sum(self.podiums_data.values())


    def get_poles(self, constructor: Constructors) -> int:
        """
        Get number of pole positions won by constructor

        Args:
            constructor (Constructors): constructor object

        Returns:
            int: number of pole positions
        """
        temp = constructor.qualifying_set.filter(position=1).count()
        return temp


    def get_drivers_info(self, instance: Constructors) -> dict[int, list]:
        """
        Return dict containing lists of drivers racing for the team per year

        Args:
            instance (_type_): driver object

        Returns:
            dict: dict containing lists of drivers racing for the team per year
        """
        query = instance.results_set.values_list("race__year", "driver__driverref").distinct()
        years_active = {year for year, driver in query}        # years of activity in F1 for driver
        result = {year: [] for year in years_active}
        for year, driver in query:
            driver_url = reverse("driver-detail", args=(driver,))
            result[year].append(driver_url)
        return result


    def get_championship_info(self, instance: Constructors) -> list[int]:
        """
        Get list of years when the team won championship(WDC)

        Args:
            instance (_type_): _description_

        Returns:
            list[int]: list of championship winning seasons for the team
        """
        try:
            team_result = ConstructorStandings.objects.filter(constructor=instance, position=1).filter(self.condition).order_by("race__year").values("race__year", "position")        
            return [k["race__year"] for k in team_result]
        except:
            return []


    def get_points_info(self, instance: Constructors) -> int | None:
        """
        Return info about all points scored by driver during the career

        Args:
            instance (_type_): constructor object

        Returns:
            int | None: amount of points constructor scored summary
        """
        try:
            constructor_results = ConstructorStandings.objects.filter(constructor=instance).filter(self.condition).aggregate(Sum("points"))
            return constructor_results["points__sum"]
        except:
            return None


    def to_representation(self, instance: Constructors) -> OrderedDict:
        """
        Add extra fields to serializer
        """
        representation = super().to_representation(instance)

        season_results = ConstructorStandings.objects.filter(constructor=instance).\
            values("race__year").annotate(last_round=Max("race__round"))
        self.condition = q_or([Q(race__round=k["last_round"], race__year=k["race__year"]) for k in season_results])
        podiums_data = instance.results_set.filter(Q(position=1) | Q(position=2) | Q(position=3)).values("position").annotate(count=Count("position")).order_by("position")
        self.podiums_data = {k["position"]: k["count"] for k in podiums_data}

        representation["wins"] = self.get_wins(instance)
        representation["podiums"] = self.get_podiums(instance)
        representation["drivers"] = self.get_drivers_info(instance)
        representation["championships"] = self.get_championship_info(instance)
        representation["points"] = self.get_points_info(instance)
        return representation


    class Meta:
        model = Constructors
        fields = ["url", "name", "nationality", "url", "poles"]


from rest_framework import serializers
from .models import Constructors, Drivers
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.reverse import reverse




class DriverSerializer(serializers.ModelSerializer):
    wins = serializers.SerializerMethodField("get_wins")
    podiums = serializers.SerializerMethodField("get_podiums")
    poles = serializers.SerializerMethodField("get_poles")
    age = serializers.SerializerMethodField("get_current_age")

    def get_wins(self, driver: Drivers) -> int:
        """
        Get number of won races

        Args:
            driver (Drivers): driver object
        Returns:
            int: number won races
        """
        temp = driver.results_set.filter(position=1).count()
        return temp

    def get_podiums(self, driver: Drivers) -> int:
        """
        Get number of podiums

        Args:
            driver (Drivers): driver object
        Returns:
            int: number of races finished on podium 
        """
        temp = driver.results_set.filter(Q(position=1) | Q(position=2) | Q(position=3)).count()
        return temp

    def get_poles(self, driver: Drivers) -> int:
        """
        Get number of pole positionss

        Args:
            driver (Drivers): driver object

        Returns:
            int: amount of won pole positions
        """
        temp = driver.qualifying_set.filter(position=1).count()
        return temp

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

    class Meta:
        model = Drivers
        fields = ["code", "number", "forename", "surname", "age", "dob", "nationality", "url", "podiums", "wins", "poles"]#, "teams"]


    def get_teams_info(self, instance) -> dict:
        """
        Return dict containing lists of teams driver was racing for per season

        Args:
            instance (_type_): constructor object

        Returns:
            dict: dict containing lists of teams driver was racing for per season
        """
        query = instance.results_set.values_list("race__year", "constructor").distinct()
        years_active = {year for year, constructor in query}        # years of activity in F1 for driver
        result = {year: [] for year in years_active}
        for year, constructor in query:
            constructor_url = reverse("constructor-detail", args=(constructor,))
            result[year].append(constructor_url)
        return result

    def get_championships_info(self, instance) -> list[int]:
        """
        Get list of championship winning seasons for the driver

        Args:
            instance (_type_): driver object

        Returns:
            list[int]: list of championship winning seasons
        """
        query = instance.results_set.race_set.

    def to_representation(self, instance):
        """
        Add info about teams driver was racing for each season
        """
        representation =  super().to_representation(instance)       # default representation
        representation["teams"] = self.get_teams_info(instance)        # add info to representation
        return representation



class ConstructorSerializer(serializers.ModelSerializer):
    wins = serializers.SerializerMethodField()
    podiums = serializers.SerializerMethodField()
    poles = serializers.SerializerMethodField()

    def get_wins(self, constructor: Constructors) -> int:
        """
        Get number of won races

        Args:
            constructor (Constructors): constructor object

        Returns:
            int: number of won races
        """
        temp = constructor.results_set.filter(position=1).count()
        return temp

    def get_podiums(self, constructor: Constructors) -> int:
        """
        Get number of podiums

        Args:
            constructor (Constructors): constructor object

        Returns:
            int: number of races finished on podium
        """
        temp = constructor.results_set\
            .filter(Q(position=1) | Q(position=2) | Q(position=3)).count()
        return temp

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

    def get_drivers_info(self, instance) -> dict:
        """
        Return dict containing lists of drivers racing for the team per year

        Args:
            instance (_type_): driver object

        Returns:
            dict: dict containing lists of drivers racing for the team per year
        """
        query = instance.results_set.values_list("race__year", "driver").distinct()
        years_active = {year for year, driver in query}        # years of activity in F1 for driver
        result = {year: [] for year in years_active}
        for year, driver in query:
            driver_url = reverse("driver-detail", args=(driver,))
            result[year].append(driver_url)
        return result

    def get_championship_info(self, instance) -> list[int]:
        """
        Get list of years when the team won championship(WDC)

        Args:
            instance (_type_): _description_

        Returns:
            list[int]: list of championship winning seasons for the team
        """
        # query = instance.result_set


        return 0


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["drivers"] = self.get_drivers_info(instance)
        representation["championships"] = self.get_championship_info(instance)
        return representation

    class Meta:
        model = Constructors
        fields = ["id", "name", "nationality", "url", "wins", "podiums", "poles"]



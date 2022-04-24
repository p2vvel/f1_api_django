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


    def to_representation(self, instance):
        """
        Add info about teams driver was racing for each season
        """
        representation =  super().to_representation(instance)       # default representation
        query = instance.results_set.values_list("race__year", "constructor").distinct()
        years_active = {year for year, constructor in query}        # years of activity in F1 for driver
        result = {year: [] for year in years_active}
        
        for year, constructor in query:
            constructor_url = reverse("constructor-detail", args=(constructor,))
            result[year].append(constructor_url)
        representation["teams"] = result        # add info to representation
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


    class Meta:
        model = Constructors
        fields = ["id", "name", "nationality", "url", "wins", "podiums", "poles"]



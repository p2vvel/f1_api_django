from rest_framework import serializers
from .models import Constructors, Drivers
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta



class DriverSerializer(serializers.ModelSerializer):
    wins = serializers.SerializerMethodField("get_wins")
    podiums = serializers.SerializerMethodField("get_podiums")
    poles = serializers.SerializerMethodField("get_poles")
    age = serializers.SerializerMethodField("get_current_age")
    teams = serializers.SerializerMethodField("get_teams")

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
        """Get number of podiums

        Args:
            driver (Drivers): driver object
        Returns:
            int: number of races ended on podium 
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

    def get_teams(self, driver: Drivers):
        """
        Get info about teams driver was racing for each season

        Args:
            driver (Drivers): driver object

        Returns:
            list[dict]: list containing dicts in format {"year": ..., "teams": [...]}
        """
        temp = driver.results_set.order_by("race__year")
        return TeamPerSeasonSerializer(temp, many=True, context=self.context).data

    class Meta:
        model = Drivers
        fields = ["code", "number", "forename", "surname", "age", "dob", "nationality", "url", "podiums", "wins", "poles", "teams"]



class ConstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Constructors
        fields = ["id", "name", "nationality", "url"]



class TeamPerSeasonSerializer(serializers.Serializer):
    year = serializers.IntegerField(source="race.year")
    constructor = serializers.HyperlinkedRelatedField(view_name="constructor-detail", read_only=True)
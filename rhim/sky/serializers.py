from rest_framework import serializers

from sky.models import Planet, Asteroid


class PlanetSerializer(serializers.ModelSerializer):
    moons_count = serializers.IntegerField()
    smallest_moon_mass = serializers.IntegerField()
    second_smallest_moon_mass = serializers.IntegerField()
    biggest_moon_mass = serializers.IntegerField()
    polar_radius_in_miles = serializers.FloatField()

    class Meta:
        model = Planet
        fields = ['name', 'polar_radius_in_miles', 'moons_count', 'smallest_moon_mass', 'second_smallest_moon_mass', 'biggest_moon_mass']


class AsteroidSerializer(serializers.ModelSerializer):
    mass_in_lbs = serializers.FloatField()

    class Meta:
        model = Asteroid
        fields = ['name', 'mass_in_lbs']
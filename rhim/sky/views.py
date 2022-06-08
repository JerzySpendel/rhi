from django.db.models import F, Count, OuterRef, Subquery
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer

from sky.models import Planet, Moon, Asteroid
from sky.serializers import PlanetSerializer, AsteroidSerializer


class PlanetsView(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    renderer_classes = [CSVRenderer, JSONRenderer]

    def get_queryset(self):
        moon_filter = Moon.objects.filter(planet=OuterRef("pk")).filter(
            mass__isnull=False
        )
        return (
            super()
            .get_queryset()
            .annotate(
                polar_radius_in_miles=F("polar_radius") / 1609.344,
                moons_count=Count("moons"),
                smallest_moon_mass=Subquery(
                    moon_filter.order_by("polar_radius").values("mass")[:1]
                ),
                second_smallest_moon_mass=Subquery(
                    moon_filter.order_by("polar_radius").values("mass")[1:2]
                ),
                biggest_moon_mass=Subquery(
                    moon_filter.order_by("-polar_radius").values("mass")[:1]
                ),
            )
            .order_by("name")
        )


class AsteroidsView(generics.ListAPIView):
    queryset = Asteroid.objects.all()
    serializer_class = AsteroidSerializer
    renderer_classes = [CSVRenderer, JSONRenderer]

    def get_queryset(self):
        venus_mass = Planet.objects.filter(name="Venus").get().mass
        return (
            super()
            .get_queryset()
            .filter(mass__gt=venus_mass)
            .annotate(mass_in_lbs=F("mass") * 0.45359237)
        )

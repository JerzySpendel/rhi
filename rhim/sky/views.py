from django.db.models import F, Count, Value, OuterRef, Subquery
from rest_framework import generics
from rest_framework_csv.renderers import CSVRenderer

from sky.models import Planet, Moon
from sky.serializers import PlanetSerializer


class PlanetsView(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    renderer_classes = [CSVRenderer]

    def get_queryset(self):
        return super().get_queryset().annotate(
            polar_radius_in_miles=F("polar_radius") / 1609.344,
            moons_count=Count("moons"),
            smallest_moon_mass=Subquery(Moon.objects.filter(planet=OuterRef('pk')).order_by('mass').values('mass')[:1]),
            second_smallest_moon_mass=Subquery(Moon.objects.filter(planet=OuterRef('pk')).order_by('mass').values('mass')[1:2]),
            biggest_moon_mass=Subquery(Moon.objects.filter(planet=OuterRef('pk')).order_by('-mass').values('mass')[:1]),
        )

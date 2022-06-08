from django.core.management.base import BaseCommand

from sky.models import Planet, Moon, Asteroid
from tools.core import Sky, Asteroid as AsteroidRaw

import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        Moon.objects.all().delete()
        Planet.objects.all().delete()
        Asteroid.objects.all().delete()

        data = requests.get("https://api.le-systeme-solaire.net/rest/bodies").json()
        sky = Sky.from_raw(data)

        for raw_planet in sky.get_planets():
            orm_planet = Planet.objects.create(name=raw_planet.name, polar_radius=raw_planet.polar_radius,
                                               mass=raw_planet.mass)
            Moon.objects.bulk_create([Moon(mass=raw_moon.mass, planet=orm_planet, polar_radius=raw_moon.polar_radius) for raw_moon in raw_planet.moons])

        Asteroid.objects.bulk_create(
            [Asteroid(mass=asteroid_raw.mass,
                      name=asteroid_raw.name) for asteroid_raw in AsteroidRaw.from_raw(data)]
        )

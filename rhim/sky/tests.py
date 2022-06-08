from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sky.models import Planet, Moon, Asteroid


class ConversionTestCase(APITestCase):
    def test_polar_radius_unit_conversion(self):
        earth_polar_radius = 6356752
        Planet.objects.create(name="Earth", polar_radius=earth_polar_radius)
        response = self.client.get(reverse('planets'))
        self.assertEqual(response.status_code, 200)
        earth_data = response.data[0]

        self.assertAlmostEqual(earth_data['polar_radius_in_miles'], earth_polar_radius / 1609.344)

    def test_getting_second_smallest_moon(self):
        planet = Planet.objects.create(name="asdf", polar_radius=1)
        Moon.objects.create(planet=planet, mass=2, polar_radius=1)
        Moon.objects.create(planet=planet, mass=1, polar_radius=2)

        response = self.client.get(reverse('planets'))
        self.assertEqual(response.status_code, 200)
        planet_data = response.data[0]

        self.assertEqual(planet_data['second_smallest_moon_mass'], 1)


class AsteroidsTestCase(APITestCase):
    def test_asteroids_bigger_than_venus(self):
        Planet.objects.create(name='Venus', mass=100, polar_radius=1)
        for mass in [10, 50, 200]:
            Asteroid.objects.create(name=str(mass), mass=mass)

        response = self.client.get(reverse('asteroids'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

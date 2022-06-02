import math
from operator import attrgetter
from typing import Iterable, Reversible

import requests
import dataclasses
import csv

data = requests.get("https://api.le-systeme-solaire.net/rest/bodies").json()


@dataclasses.dataclass
class Moon:
    mass: float


@dataclasses.dataclass
class Planet:
    id: str
    name: str
    polar_radius: float
    moons: list[Moon] = dataclasses.field(default_factory=list)

    def biggest(self) -> Iterable[Moon]:
        return reversed(self.smallest())

    def smallest(self) -> Iterable[Moon] | Reversible[Moon]:
        return sorted(self.moons, key=attrgetter('mass'))


class Sky:
    def __init__(self, planets: list[Planet]):
        self.planets = planets

    @classmethod
    def from_raw(cls, data: dict) -> 'Sky':
        bodies = data['bodies']
        planets = []

        planets_raw = list(filter(lambda body: body['bodyType'] == 'Planet', bodies))
        moons_raw = list(filter(lambda body: body['bodyType'] == 'Moon', bodies))

        for planet_raw in planets_raw:
            planet = Planet(
                id=planet_raw['id'],
                name=planet_raw['englishName'],
                polar_radius=planet_raw['polarRadius'],
                moons=[],
            )
            moons = []
            for moon_raw in filter(lambda moon_raw: moon_raw['aroundPlanet']['planet'] == planet.id, moons_raw):
                if mass_data := moon_raw.get('mass'):
                    mass = mass_data['massValue'] * 10 ** mass_data['massExponent']
                else:
                    mass = math.nan

                moons.append(
                    Moon(mass=mass)
                )

            planet.moons = moons
            planets.append(planet)

        return Sky(planets)

    @classmethod
    def from_list(cls, planet_list: list[Planet]) -> 'Sky':
        pass

    def to_csv(self):
        file = open('planets.cvs', 'w', newline='')
        fieldnames = ['name', 'moons_count', 'smallest_moon_mass', 'second_smallest_moon_mass', 'biggest_moon_mass', 'polar_radius']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for planet in self.planets:
            row = {
                'name': planet.name,
                'moons_count': len(planet.moons),
                'polar_radius': planet.polar_radius / 1609.344
            }

            moons_masses = [moon.mass for moon in planet.moons]
            smallest_masses = iter(sorted(moons_masses))
            row['smallest_moon_mass'] = next(smallest_masses, None)
            row['second_smallest_moon_mass'] = next(smallest_masses, None)
            row['biggest_moon_mass'] = next(iter(sorted(moons_masses, reverse=True)), None)

            csv_writer.writerow(row)


sky = Sky.from_raw(data)
sky.to_csv()
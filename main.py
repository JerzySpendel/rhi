import math

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


class Sky:
    def __init__(self, planets: list[Planet]):
        self.planets = planets

    @classmethod
    def from_raw(cls, data: dict) -> 'Sky':
        bodies = data['bodies']
        planets = []

        planets_raw = [body for body in bodies if body['bodyType'] == 'Planet']
        moons_raw = [body for body in bodies if body['bodyType'] == 'Moon']

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

    def get_planet(self, name: str) -> Planet | None:
        return next((planet for planet in self.planets if planet.name == name))

    def to_csv(self):
        file = open('planets.csv', 'w', newline='')
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
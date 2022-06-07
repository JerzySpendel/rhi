import dataclasses
import math


class Entity:
    def __init__(self, entity_data: dict):
        self.data = entity_data

    @property
    def mass(self) -> float | None:
        if mass_data := self.data.get('mass'):
            return mass_data['massValue'] * 10 ** (mass_data['massValue'])

    @property
    def polar_radius(self) -> float:
        return self.data['polarRadius'] / 1.609344


@dataclasses.dataclass
class Moon:
    mass: float


@dataclasses.dataclass
class Planet:
    id: str
    name: str
    polar_radius: float
    moons: list[Moon] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Asteroid:
    name: str
    mass: float

    @classmethod
    def from_raw(cls, data: dict) -> list['Self']:
        asteroids_raw = [entry for entry in data['bodies'] if entry['bodyType'] == 'Asteroid']
        return [Asteroid(name=asteroid_raw['name'], mass=Entity(asteroid_raw).mass) for asteroid_raw in asteroids_raw]


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

    def get_planets(self) -> list[Planet]:
        return self.planets
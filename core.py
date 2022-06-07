import dataclasses
import math


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

    def get_planets(self) -> list[Planet]:
        return self.planets
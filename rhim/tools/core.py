import dataclasses


class Entity:
    def __init__(self, entity_data: dict):
        self.data = entity_data

    @property
    def mass(self) -> float | None:
        if mass_data := self.data.get("mass"):
            return mass_data["massValue"] * 10 ** (mass_data["massExponent"])

    @property
    def polar_radius(self) -> float:
        return self.data["polarRadius"] * 1000


@dataclasses.dataclass
class Moon:
    mass: float
    polar_radius: float


def load_planets(data: dict) -> list['Planet']:
    bodies = data["bodies"]
    planets = []

    planets_raw = [body for body in bodies if body["bodyType"] == "Planet"]
    moons_raw = [body for body in bodies if body["bodyType"] == "Moon"]

    for planet_raw in planets_raw:
        planet = Planet(
            id=planet_raw["id"],
            name=planet_raw["englishName"],
            polar_radius=Entity(planet_raw).polar_radius,
            mass=Entity(planet_raw).mass,
            moons=[],
        )
        moons = []

        for moon_raw in filter(
                lambda moon_raw: moon_raw["aroundPlanet"]["planet"] == planet.id,
                moons_raw,
        ):
            mass = Entity(moon_raw).mass
            if not mass:
                continue

            moons.append(
                Moon(
                    mass=mass,
                    polar_radius=Entity(moon_raw).polar_radius,
                )
            )

        planet.moons = moons
        planets.append(planet)

    return planets


@dataclasses.dataclass
class Planet:
    id: str
    name: str
    polar_radius: float
    mass: float
    moons: list[Moon] = dataclasses.field(default_factory=list)

    def __post_init__(self, *args, **kwargs):
        self.moons = sorted([moon for moon in self.moons if moon.mass], key=lambda moon: moon.polar_radius)

    def _smallest_moon_mass(self) -> float | None:
        if not self.moons:
            return

        return self.moons[0].mass

    def _second_smallest_moon_mass(self) -> float | None:
        if not len(self.moons) >= 2:
            return

        return self.moons[1].mass

    def _biggest_moon_mass(self) -> float | None:
        if not self.moons:
            return

        return self.moons[-1].mass

    @classmethod
    def csv_fields(cls) -> list[str]:
        return ['name', 'moons_count', 'smallest_moon_mass', 'second_smallest_moon_mass', 'biggest_moon_mass', 'polar_radius_in_miles']

    def csv_row(self) -> dict:
        return {
            'name': self.name,
            'moons_count': len(self.moons),
            'smallest_moon_mass': self._smallest_moon_mass(),
            'second_smallest_moon_mass': self._second_smallest_moon_mass(),
            'biggest_moon_mass': self._biggest_moon_mass(),
            'polar_radius_in_miles': self.polar_radius / 1609.344
        }


@dataclasses.dataclass
class Asteroid:
    name: str
    mass: float

    @classmethod
    def csv_fields(cls):
        return ['name', 'mass']

    def csv_row(self) -> dict:
        return {
            'name': self.name,
            'mass': self.mass * 2.204,
        }


def load_asteroids(data: dict) -> list["Asteroid"]:
    asteroids_raw = [
        entry for entry in data["bodies"] if entry["bodyType"] == "Asteroid"
    ]

    return [
        Asteroid(name=asteroid_raw["name"], mass=Entity(asteroid_raw).mass)
        for asteroid_raw in asteroids_raw
    ]

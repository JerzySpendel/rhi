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


@dataclasses.dataclass
class Planet:
    id: str
    name: str
    polar_radius: float
    mass: float
    moons: list[Moon] = dataclasses.field(default_factory=list)

    @classmethod
    def from_raw(cls, data: dict) -> list['Planet']:
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
                moons.append(
                    Moon(
                        mass=Entity(moon_raw).mass,
                        polar_radius=Entity(moon_raw).polar_radius,
                    )
                )

            planet.moons = moons
            planets.append(planet)

        return planets


@dataclasses.dataclass
class Asteroid:
    name: str
    mass: float

    @classmethod
    def from_raw(cls, data: dict) -> list["Asteroid"]:
        asteroids_raw = [
            entry for entry in data["bodies"] if entry["bodyType"] == "Asteroid"
        ]
        return [
            Asteroid(name=asteroid_raw["name"], mass=Entity(asteroid_raw).mass)
            for asteroid_raw in asteroids_raw
        ]

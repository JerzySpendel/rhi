import requests

from tools.core import Planet, Entity, Moon, Asteroid


class Database:
    planets = None
    asteroids = None
    _instance = None

    @classmethod
    def get(cls) -> "Database":
        if cls._instance:
            return cls._instance

        instance = Database()
        api_data = requests.get("https://api.le-systeme-solaire.net/rest/bodies").json()
        instance.planets = cls.load_planets(api_data)
        instance.asteroids = cls.load_asteroids(api_data)
        cls._instance = instance

        return cls._instance

    @classmethod
    def load_planets(cls, data: dict) -> list["Planet"]:
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

    @classmethod
    def load_asteroids(cls, data: dict) -> list["Asteroid"]:
        asteroids_raw = [
            entry for entry in data["bodies"] if entry["bodyType"] == "Asteroid"
        ]

        return [
            Asteroid(name=asteroid_raw["name"], mass=Entity(asteroid_raw).mass)
            for asteroid_raw in asteroids_raw
        ]

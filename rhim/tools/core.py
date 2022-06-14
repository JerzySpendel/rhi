import dataclasses

from tools.constants import METER_TO_MIL, KG_TO_POUND


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

    def __post_init__(self, *args, **kwargs):
        self.moons = sorted(
            [moon for moon in self.moons if moon.mass],
            key=lambda moon: moon.polar_radius,
        )

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
        return [
            "name",
            "moons_count",
            "smallest_moon_mass",
            "second_smallest_moon_mass",
            "biggest_moon_mass",
            "polar_radius_in_miles",
        ]

    def csv_row(self) -> dict:
        return {
            "name": self.name,
            "moons_count": len(self.moons),
            "smallest_moon_mass": self._smallest_moon_mass(),
            "second_smallest_moon_mass": self._second_smallest_moon_mass(),
            "biggest_moon_mass": self._biggest_moon_mass(),
            "polar_radius_in_miles": self.polar_radius * METER_TO_MIL,
        }


@dataclasses.dataclass
class Asteroid:
    name: str
    mass: float

    @classmethod
    def csv_fields(cls):
        return ["name", "mass"]

    def csv_row(self) -> dict:
        return {
            "name": self.name,
            "mass": self.mass * KG_TO_POUND,
        }

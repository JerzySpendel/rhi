import pytest

from tools.constants import METER_TO_MIL
from tools.core import Planet, Moon
from tools.database import Database


@pytest.fixture()
def api_data():
    return {
        'bodies': [
            {
                "id": "lune",
                "name": "La Lune",
                "englishName": "Moon",
                "isPlanet": False,
                "moons": None,
                "mass": {
                    "massValue": 7.346,
                    "massExponent": 22
                },
                "vol": {
                    "volValue": 2.1968,
                    "volExponent": 10
                },
                "polarRadius": 1736,
                "aroundPlanet": {
                    "planet": "terre",
                    "rel": "https://api.le-systeme-solaire.net/rest/bodies/terre"
                },
                "bodyType": "Moon",
            },
            {
                "id": "terre",
                "name": "La Terre",
                "englishName": "Earth",
                "isPlanet": True,
                "moons": [
                    {
                        "moon": "La Lune",
                        "rel": "https://api.le-systeme-solaire.net/rest/bodies/lune"
                    }
                ],
                "mass": {
                    "massValue": 5.97237,
                    "massExponent": 24
                },
                "vol": {
                    "volValue": 1.08321,
                    "volExponent": 12
                },
                "polarRadius": 6356.8,
                "aroundPlanet": None,
                "bodyType": "Planet"
            }
        ]
    }


@pytest.fixture()
def planet() -> Planet:
    return Planet(
        name='adf',
        id='adsf',
        polar_radius=1,
        mass=1,
        moons=[Moon(mass=1, polar_radius=1),
               Moon(mass=2, polar_radius=2)]
    )


def test_polar_radius_conversion(planet: Planet):
    assert planet.csv_row()['polar_radius_in_miles'] == planet.polar_radius * METER_TO_MIL


def test_getting_second_smallest_moon(planet: Planet):
    assert planet.csv_row()['second_smallest_moon_mass'] == planet.moons[1].mass


def test_loading_planets(api_data):
    planets = Database.load_planets(api_data)

    assert len(planets) == 1
    assert len(planets[0].moons) == 1


def test_request_is_sent_once(mocker, api_data):
    json = mocker.patch('tools.database.requests').get().json
    json.return_value = api_data
    for _ in range(10):
        Database.get()

    json.assert_called_once()
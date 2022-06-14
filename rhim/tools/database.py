import requests

from tools.core import load_planets, load_asteroids


class Database:
    planets = None
    asteroids = None
    _instance = None

    @classmethod
    def get(cls) -> 'Database':
        if cls._instance:
            return cls._instance

        instance = Database()
        r = requests.get('https://api.le-systeme-solaire.net/rest/bodies').json()
        instance.planets = load_planets(r)
        instance.asteroids = load_asteroids(r)
        cls._instance = instance

        return cls._instance


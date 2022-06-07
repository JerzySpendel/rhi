import csv
import requests

from core import Sky

data = requests.get("https://api.le-systeme-solaire.net/rest/bodies").json()
sky = Sky.from_raw(data)

file = open('planets.csv', 'w', newline='')
fieldnames = ['name', 'moons_count', 'smallest_moon_mass', 'second_smallest_moon_mass', 'biggest_moon_mass',
              'polar_radius']
csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

csv_writer.writeheader()

for planet in sky.get_planets():
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

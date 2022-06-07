from django.db import models


class Planet(models.Model):
    name = models.TextField()
    mass = models.FloatField(null=True)
    polar_radius = models.FloatField()


class Moon(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name="moons")
    mass = models.FloatField(null=True)


class Asteroid(models.Model):
    name = models.TextField()
    mass = models.FloatField(null=True)

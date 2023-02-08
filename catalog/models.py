from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Musician(AbstractUser):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    genres = models.ManyToManyField(Genre, related_name="bands")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bands")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} form {self.country}. ({self.description})"

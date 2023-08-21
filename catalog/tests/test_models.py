from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import (
    Band,
    Genre,
    Instrument,
    Country
)

GENRE_NAME = "Art rock"
COUNTRY_NAME = "Sweden"
INSTRUMENT_NAME = "Guitar"

USERNAME = "admin"
PASSWORD = "test12345"
FIRST_NAME = "John"
LAST_NAME = "Petrucci"
EMAIL = "John.Petrucci@music.world"

BAND_NAME = "Dream Theater"
BAND_DESCRIPTION = "Test description"


class GenreModelTests(TestCase):
    def test_str_in_genre_model(self):
        genre = Genre.objects.create(name=GENRE_NAME)
        self.assertEqual(str(genre), f"{genre.name}")


class CountryModelTests(TestCase):
    def setUp(self):
        Country.objects.create(name=COUNTRY_NAME)

        self.country = Country.objects.get(name=COUNTRY_NAME)

    def test_str_in_country_model(self):
        self.assertEqual(str(self.country), f"{self.country.name}")

    def test_verbose_names_labels_in_country_model(self):
        self.assertEqual(self.country._meta.verbose_name, "country")
        self.assertEqual(self.country._meta.verbose_name_plural, "countries")


class InstrumentModelTests(TestCase):
    def test_str_in_instrument_model(self):
        instrument = Instrument.objects.create(name=INSTRUMENT_NAME)

        self.assertEqual(str(instrument), f"{instrument.name}")


class MusicianModelTests(TestCase):
    def setUp(self):
        instrument = Instrument.objects.create(name=INSTRUMENT_NAME)

        self.musician = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            instrument=instrument
        )

    def test_create_musician_with_instrument(self):
        self.assertEqual(self.musician.username, USERNAME)
        self.assertTrue(self.musician.check_password(PASSWORD))
        self.assertEqual(self.musician.first_name, FIRST_NAME)
        self.assertEqual(self.musician.last_name, LAST_NAME)
        self.assertEqual(self.musician.email, EMAIL)
        self.assertEqual(self.musician.instrument.name, INSTRUMENT_NAME)

    def test_str_in_musician_model(self):
        self.assertEqual(
            str(self.musician),
            f"{self.musician.first_name} {self.musician.last_name}"
        )


class BandModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name=GENRE_NAME)
        self.country = Country.objects.create(name=COUNTRY_NAME)
        instrument = Instrument.objects.create(name=INSTRUMENT_NAME)

        self.musician = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            instrument=instrument,
        )

        self.band = Band.objects.create(
            name=BAND_NAME,
            description=BAND_DESCRIPTION,
            country=self.country,
        )

        self.band.genres.add(self.genre)
        self.band.members.add(self.musician)

    def test_fields_in_band_model(self):
        self.assertEqual(self.band.name, BAND_NAME)
        self.assertEqual(self.band.description, BAND_DESCRIPTION)
        self.assertEqual(self.band.country.name, COUNTRY_NAME)
        self.assertEqual(self.band.genres.get(name=GENRE_NAME), self.genre)
        self.assertEqual(self.band.members.get(username=USERNAME), self.musician)

    def test_country_genres_and_members_labels_in_car_model(self):
        country_label = self.band._meta.get_field("country").verbose_name
        genres_label = self.band._meta.get_field("genres").verbose_name
        members_label = self.band._meta.get_field("members").verbose_name
        self.assertEqual(country_label, "country")
        self.assertEqual(genres_label, "genres")
        self.assertEqual(members_label, "members")

    def test_str_in_band_model(self):
        self.assertEqual(str(self.band), self.band.name)

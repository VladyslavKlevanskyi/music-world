from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import (
    Band,
    Genre,
    Instrument,
    Country
)

INDEX_URL = reverse("catalog:index")


class LoginRequiredTest(TestCase):
    def test_login_required_for_index(self):
        response = self.client.get(INDEX_URL)

        self.assertNotEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_genres = 2
        number_of_instruments = 2
        number_of_musicians = 2
        number_of_bands = 2

        country = Country.objects.create(name="China")

        for genre_id in range(number_of_genres):
            Genre.objects.create(
                name=f"Genre {genre_id}",
            )

        for instrument_id in range(number_of_instruments):
            Instrument.objects.create(
                name=f"Instrument {instrument_id}",
            )

        for musician_id in range(number_of_musicians):
            get_user_model().objects.create_user(
                username=f"Username {musician_id}",
                password="1qazXcde3",
                instrument=Instrument.objects.get(name="Instrument 1")
            )

        for band_id in range(number_of_bands):
            Band.objects.create(
                name=f"Band {band_id}",
                description=f"Description {band_id}",
                country=country,
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345",
            instrument=Instrument.objects.get(name="Instrument 1")
        )
        self.client.force_login(self.user)
        self.response = self.client.get(INDEX_URL)

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "catalog/index.html")

    def test_index_view_shows_correct_content(self):
        num_bands = self.response.context["num_bands"]
        num_musicians = self.response.context["num_musicians"]
        num_genres = self.response.context["num_genres"]
        num_instruments = self.response.context["num_instruments"]

        self.assertEqual(num_bands, 2)
        self.assertEqual(num_musicians, 3)
        self.assertEqual(num_genres, 2)
        self.assertEqual(num_instruments, 2)

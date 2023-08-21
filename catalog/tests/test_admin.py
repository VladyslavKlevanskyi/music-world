from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Instrument

INSTRUMENT_NAME = "Guitar"

USERNAME = "musician_username"
PASSWORD = "test12345"
FIRST_NAME = "John"
LAST_NAME = "Petrucci"
EMAIL = "John.Petrucci@music.world"


class MusicianAdminTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name=INSTRUMENT_NAME)

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin_pass",
            instrument=self.instrument
        )
        self.client.force_login(self.admin_user)

        self.musician = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            instrument=self.instrument
        )

    def test_musician_instrument_listed(self):
        url = reverse("admin:catalog_musician_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.musician.instrument)

    def test_musician_detailed_instrument_listed(self):
        url = reverse("admin:catalog_musician_change", args=[self.musician.id])
        response = self.client.get(url)

        self.assertContains(response, self.musician.instrument)

    def test_musician_creation_fieldsets(self):
        form_data = {
            "username": USERNAME,
            "password1": PASSWORD,
            "password2": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "email": EMAIL,
            "instrument": self.instrument
        }

        self.client.post(reverse("admin:catalog_musician_add"), data=form_data)
        new_musician = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(
            new_musician.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_musician.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_musician.email,
            form_data["email"]
        )
        self.assertEqual(
            new_musician.instrument,
            form_data["instrument"]
        )

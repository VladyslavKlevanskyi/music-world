from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Instrument

INSTRUMENTS_LIST_URL = reverse("catalog:instrument-list-view")
INSTRUMENTS_CREATE_URL = reverse("catalog:instrument-create")


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name="Instrument-Test")

    def test_login_required_for_country_instrument_view(self):
        response = self.client.get(INSTRUMENTS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_instrument_create(self):
        response = self.client.get(INSTRUMENTS_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_instrument_update(self):
        response = self.client.get(reverse(
            "catalog:instrument-update",
            args=[self.instrument.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_instrument_delete(self):
        response = self.client.get(reverse(
            "catalog:instrument-delete",
            args=[self.instrument.id])
        )
        self.assertNotEqual(response.status_code, 200)


class InstrumentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_instruments = 10

        for instrument_id in range(number_of_instruments):
            Instrument.objects.create(name=f"Instrument {instrument_id}")

    def setUp(self) -> None:
        instrument = Instrument.objects.create(name="Guitar")

        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345",
            instrument=instrument
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(INSTRUMENTS_LIST_URL)
        self.create_response = self.client.get(INSTRUMENTS_CREATE_URL)
        self.update_response = self.client.get(reverse(
            "catalog:instrument-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "catalog:instrument-delete", args=[1])
        )

    def test_retrieve_instrument_list_view(self):
        response = self.client.get(INSTRUMENTS_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_instrument_create(self):
        response = self.client.get(INSTRUMENTS_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_instrument_update(self):
        response = self.client.get(reverse(
            "catalog:instrument-update",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_instrument_delete(self):
        response = self.client.get(reverse(
            "catalog:instrument-delete",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_instrument_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/instruments/")
        create_view_response = self.client.get("/instruments/create/")
        update_view_response = self.client.get("/instruments/1/update/")
        delete_view_response = self.client.get("/instruments/1/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_instrument_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_instrument_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "catalog/instrument_list.html"
        )
        self.assertTemplateUsed(
            self.create_response,
            "catalog/instrument_form.html"
        )

        self.assertTemplateUsed(
            self.delete_response,
            "catalog/instrument_confirm_delete.html"
        )

    def test_instrument_list_view_pagination_is_eight(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["instrument_list"]), 8
        )

    def test_instrument_list_view_lists_all_instruments(self):
        response_sec_page = self.client.get(INSTRUMENTS_LIST_URL + "?page=2")
        instruments = Instrument.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["instrument_list"]
            ) + list(
                response_sec_page.context["instrument_list"]
            ), list(instruments)
        )

    def test_instrument_list_view_search(self):
        number_of_instruments = 10
        for instrument_id in range(number_of_instruments):
            Instrument.objects.create(
                name=f"TestInstrument {instrument_id}",
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/instruments/", {"name": "TestInstrument", "page": f"{page_number}"}
            )
            response_list += list(search_result.context["instrument_list"])
        filter_result = Instrument.objects.filter(
            name__icontains="TestInstrument"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_instrument_create_view_creates_new_instrument(self):
        form_data = {
            "name": "Drums",
        }
        self.client.post(reverse("catalog:instrument-create"), data=form_data)
        new_instrument = Instrument.objects.get(name=form_data["name"])

        self.assertEqual(new_instrument.name, form_data["name"])

    def test_instrument_update_view_updates_instrument(self):
        form_data = {
            "name": "Drums",
        }
        instrument_id_for_update = Instrument.objects.get(name="Instrument 1").id
        self.client.post(reverse(
            "catalog:instrument-update",
            args=[instrument_id_for_update]),
            data=form_data
        )
        updated_instrument = Instrument.objects.get(
            id=instrument_id_for_update
        )

        self.assertEqual(updated_instrument.name, form_data["name"])

    def test_instrument_delete_view_deletes_instrument(self):
        instrument_id_for_deletes = Instrument.objects.get(name="Instrument 1").id
        self.client.post(reverse(
            "catalog:instrument-delete",
            args=[instrument_id_for_deletes]
        )
        )

        self.assertEqual(list(Instrument.objects.filter(name="Instrument 1")), [])

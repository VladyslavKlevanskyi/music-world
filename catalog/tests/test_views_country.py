from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Country, Instrument

COUNTRIES_LIST_URL = reverse("catalog:country-list-view")
COUNTRIES_CREATE_URL = reverse("catalog:country-create")


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Country-Test")

    def test_login_required_for_country_list_view(self):
        response = self.client.get(COUNTRIES_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_country_create(self):
        response = self.client.get(COUNTRIES_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_country_update(self):
        response = self.client.get(reverse(
            "catalog:country-update",
            args=[self.country.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_country_delete(self):
        response = self.client.get(reverse(
            "catalog:country-delete",
            args=[self.country.id])
        )
        self.assertNotEqual(response.status_code, 200)


class CountryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_countries = 10

        for country_id in range(number_of_countries):
            Country.objects.create(name=f"Country {country_id}")

    def setUp(self) -> None:
        instrument = Instrument.objects.create(name="Guitar")

        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345",
            instrument=instrument
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(COUNTRIES_LIST_URL)
        self.create_response = self.client.get(COUNTRIES_CREATE_URL)
        self.update_response = self.client.get(reverse(
            "catalog:country-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "catalog:country-delete", args=[1])
        )

    def test_retrieve_country_list_view(self):
        response = self.client.get(COUNTRIES_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_country_create(self):
        response = self.client.get(COUNTRIES_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_country_update(self):
        response = self.client.get(reverse(
            "catalog:country-update",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_country_delete(self):
        response = self.client.get(reverse(
            "catalog:country-delete",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_country_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/countries/")
        create_view_response = self.client.get("/countries/create/")
        update_view_response = self.client.get("/countries/1/update/")
        delete_view_response = self.client.get("/countries/1/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_country_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_country_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "catalog/country_list.html"
        )
        self.assertTemplateUsed(
            self.create_response,
            "catalog/country_form.html"
        )

        self.assertTemplateUsed(
            self.delete_response,
            "catalog/country_confirm_delete.html"
        )

    def test_country_list_view_pagination_is_eight(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["country_list"]), 8
        )

    def test_country_list_view_lists_all_countries(self):
        response_sec_page = self.client.get(COUNTRIES_LIST_URL + "?page=2")
        countries = Country.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["country_list"]
            ) + list(
                response_sec_page.context["country_list"]
            ), list(countries)
        )

    def test_country_list_view_search(self):
        number_of_countries = 10
        for country_id in range(number_of_countries):
            Country.objects.create(
                name=f"TestCountry {country_id}",
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/countries/", {"name": "TestCountry", "page": f"{page_number}"}
            )
            response_list += list(search_result.context["country_list"])
        filter_result = Country.objects.filter(
            name__icontains="TestCountry"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_country_create_view_creates_new_country(self):
        form_data = {
            "name": "Georgia",
        }
        self.client.post(reverse("catalog:country-create"), data=form_data)
        new_country = Country.objects.get(name=form_data["name"])

        self.assertEqual(new_country.name, form_data["name"])

    def test_country_update_view_updates_country(self):
        form_data = {
            "name": "Georgia",
        }
        country_id_for_update = Country.objects.get(name="Country 1").id
        self.client.post(reverse(
            "catalog:country-update",
            args=[country_id_for_update]),
            data=form_data
        )
        updated_country = Country.objects.get(
            id=country_id_for_update
        )

        self.assertEqual(updated_country.name, form_data["name"])

    def test_country_delete_view_deletes_country(self):
        country_id_for_deletes = Country.objects.get(name="Country 1").id
        self.client.post(reverse(
            "catalog:country-delete",
            args=[country_id_for_deletes]
        )
        )

        self.assertEqual(list(Country.objects.filter(name="Country 1")), [])

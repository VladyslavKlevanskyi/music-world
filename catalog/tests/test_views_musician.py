from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Instrument, Musician

MUSICIANS_LIST_URL = reverse("catalog:musician-list-view")
MUSICIANS_CREATE_URL = reverse("catalog:musician-create")


class LoginRequiredTest(TestCase):
    def setUp(self):
        instrument = Instrument.objects.create(name="Guitar")
        self.musician = get_user_model().objects.create_user(
            username="U_serName",
            password="P_ass12345",
            instrument=instrument
        )

    def test_login_required_for_musician_list_view(self):
        response = self.client.get(MUSICIANS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_musician_detail_view(self):
        response = self.client.get(reverse(
            "catalog:musician-detail-view",
            args=[self.musician.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_musician_create(self):
        response = self.client.get(MUSICIANS_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_musician_update(self):
        response = self.client.get(reverse(
            "catalog:musician-update",
            args=[self.musician.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_musician_delete(self):
        response = self.client.get(reverse(
            "catalog:musician-delete",
            args=[self.musician.id])
        )
        self.assertNotEqual(response.status_code, 200)


class MusicianViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_musicians = 5
        instrument = Instrument.objects.create(name="Guitar")

        for musician_id in range(number_of_musicians):
            get_user_model().objects.create_user(
                username=f"Musician {musician_id}",
                password=f"Pass1234{musician_id}",
                first_name=f"MusicianFirstName {musician_id}",
                last_name=f"MusicianLastName {musician_id}",
                instrument=instrument
            )

    def setUp(self) -> None:
        self.instrument = Instrument.objects.create(name="Drums")

        self.user = get_user_model().objects.create_user(
            username="UserMame",
            password="Pazz12345",
            instrument=self.instrument
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(MUSICIANS_LIST_URL)
        self.create_response = self.client.get(MUSICIANS_CREATE_URL)
        self.update_response = self.client.get(reverse(
            "catalog:musician-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "catalog:musician-delete", args=[1])
        )
        self.detail_response = self.client.get(reverse(
            "catalog:musician-detail-view", args=[1])
        )

    def test_retrieve_musician_list_view(self):
        response = self.client.get(MUSICIANS_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_musician_detail_view(self):
        response = self.client.get(reverse(
            "catalog:musician-detail-view",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_musician_create(self):
        response = self.client.get(MUSICIANS_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_musician_update(self):
        response = self.client.get(reverse(
            "catalog:musician-update",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_musician_delete(self):
        response = self.client.get(reverse(
            "catalog:musician-delete",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_musician_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/musicians/")
        create_view_response = self.client.get("/musicians/create/")
        update_view_response = self.client.get("/musicians/1/update/")
        delete_view_response = self.client.get("/musicians/1/delete/")
        detail_view_response = self.client.get("/musicians/1/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)
        self.assertEqual(detail_view_response.status_code, 200)

    def test_musician_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)
        self.assertEqual(self.detail_response.status_code, 200)

    def test_musician_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "catalog/musician_list.html"
        )
        self.assertTemplateUsed(
            self.detail_response,
            "catalog/musician_detail.html"
        )
        self.assertTemplateUsed(
            self.create_response,
            "catalog/musician_form.html"
        )
        self.assertTemplateUsed(
            self.delete_response,
            "catalog/musician_confirm_delete.html"
        )

    def test_musician_list_view_pagination_is_three(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["musician_list"]), 3
        )

    def test_musician_list_view_lists_all_musicians(self):
        response_sec_page = self.client.get(MUSICIANS_LIST_URL + "?page=2")
        musicians = Musician.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["musician_list"]
            ) + list(
                response_sec_page.context["musician_list"]
            ), list(musicians)
        )

    def test_musician_list_view_search(self):
        number_of_musicians = 5

        for musician_id in range(number_of_musicians):
            get_user_model().objects.create_user(
                username=f"TestName {musician_id}",
                password="Pass12345",
                first_name=f"TestFirstName {musician_id}",
                last_name=f"TestLastName {musician_id}",
                instrument=self.instrument
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/musicians/", {
                    "musician": "TestFirstName",
                    "page": f"{page_number}"}
            )
            response_list += list(search_result.context["musician_list"])
        filter_result = Musician.objects.filter(
            first_name__icontains="TestFirstName"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_musician_create_view_creates_new_musician(self):
        form_data = {
            "username": "UserMuz",
            "password1": "23f#gf34",
            "password2": "23f#gf34",
            "first_name": "FirstMuz",
            "last_name": "LastMuz",
            "instrument": self.instrument.id
        }
        self.client.post(reverse("catalog:musician-create"), data=form_data)
        new_musician = Musician.objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_musician.username, form_data["username"])
        self.assertEqual(new_musician.first_name, form_data["first_name"])
        self.assertEqual(new_musician.last_name, form_data["last_name"])
        self.assertEqual(new_musician.instrument.id, form_data["instrument"])

    def test_musician_update_view_updates_musician(self):
        form_data = {
            "username": "UserMuz",
            "password1": "23f#gf34",
            "password2": "23f#gf34",
            "first_name": "FirstMuz",
            "last_name": "LastMuz",
            "instrument": self.instrument.id
        }
        musician_id_for_update = Musician.objects.get(username="Musician 1").id
        self.client.post(reverse(
            "catalog:musician-update",
            args=[musician_id_for_update]),
            data=form_data
        )
        updated_musician = Musician.objects.get(
            id=musician_id_for_update
        )

        self.assertEqual(updated_musician.username, form_data["username"])
        self.assertEqual(updated_musician.first_name, form_data["first_name"])
        self.assertEqual(updated_musician.last_name, form_data["last_name"])
        self.assertEqual(updated_musician.instrument.id, form_data["instrument"])

    def test_musician_delete_view_deletes_musician(self):
        musician_id_for_delete = Musician.objects.get(username="Musician 1").id
        self.client.post(reverse(
            "catalog:musician-delete",
            args=[musician_id_for_delete]
        )
        )

        self.assertEqual(list(Musician.objects.filter(username="Musician 1")), [])

    def test_musician_detail_view_show_all_content(self):
        musician = get_user_model().objects.create_user(
            username="MusicianD",
            password="Pass1234#D",
            first_name="MusicianFirstNameD",
            last_name="MusicianLastNameD",
            instrument=self.instrument
        )

        musician_context_response = self.client.get(reverse(
            "catalog:musician-detail-view",
            args=[musician.id])
        ).context["musician"]

        self.assertEqual(
            musician_context_response.username,
            musician.username
        )
        self.assertEqual(
            musician_context_response.first_name,
            musician.first_name
        )
        self.assertEqual(
            musician_context_response.last_name,
            musician.last_name
        )
        self.assertEqual(
            musician_context_response.instrument.id,
            musician.instrument.id
        )

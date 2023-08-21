from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import (
    Instrument,
    Musician,
    Band,
    Genre,
    Country
)

BANDS_LIST_URL = reverse("catalog:band-list-view")
BANDS_CREATE_URL = reverse("catalog:band-create")


class LoginRequiredTest(TestCase):
    def setUp(self):
        instrument = Instrument.objects.create(name="Guitar")
        country = Country.objects.create(name="China")
        self.musician = get_user_model().objects.create_user(
            username="U_serName",
            password="P_ass12345",
            instrument=instrument
        )
        self.band = Band.objects.create(
            name="L_Band",
            description="L_Description",
            country=country,
        )

    def test_login_required_for_band_list_view(self):
        response = self.client.get(BANDS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_band_detail_view(self):
        response = self.client.get(reverse(
            "catalog:band-detail-view",
            args=[self.band.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_band_create(self):
        response = self.client.get(BANDS_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_band_update(self):
        response = self.client.get(reverse(
            "catalog:band-update",
            args=[self.band.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_band_delete(self):
        response = self.client.get(reverse(
            "catalog:band-delete",
            args=[self.band.id])
        )
        self.assertNotEqual(response.status_code, 200)


class BandViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_bands = 7

        country = Country.objects.create(name="India")

        # instrument = Instrument.objects.create(name="Guitar")
        # musician = get_user_model().objects.create_user(
        #     username="U_serName",
        #     password="P_ass12345",
        #     instrument=instrument
        # )

        for band_id in range(number_of_bands):
            Band.objects.create(
                name=f"Band {band_id}",
                description=f"Description {band_id}",
                country=country,
            )

    def setUp(self) -> None:
        self.country = Country.objects.get(name="India")
        self.genre = Genre.objects.create(name="Pop")
        self.instrument = Instrument.objects.create(name="Drums")

        self.user = get_user_model().objects.create_user(
            username="UserMame",
            password="Pazz12345",
            instrument=self.instrument
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(BANDS_LIST_URL)
        self.create_response = self.client.get(BANDS_CREATE_URL)
        self.update_response = self.client.get(reverse(
            "catalog:band-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "catalog:band-delete", args=[1])
        )
        self.detail_response = self.client.get(reverse(
            "catalog:band-detail-view", args=[1])
        )

    def test_retrieve_band_list_view(self):
        response = self.client.get(BANDS_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_band_detail_view(self):
        response = self.client.get(reverse(
            "catalog:band-detail-view",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_band_create(self):
        response = self.client.get(BANDS_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_band_update(self):
        response = self.client.get(reverse(
            "catalog:musician-update",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_band_delete(self):
        response = self.client.get(reverse(
            "catalog:band-delete",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_band_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/bands/")
        create_view_response = self.client.get("/bands/create/")
        update_view_response = self.client.get("/bands/1/update/")
        delete_view_response = self.client.get("/bands/1/delete/")
        detail_view_response = self.client.get("/bands/1/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)
        self.assertEqual(detail_view_response.status_code, 200)

    def test_band_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)
        self.assertEqual(self.detail_response.status_code, 200)

    def test_band_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "catalog/band_list.html"
        )
        self.assertTemplateUsed(
            self.detail_response,
            "catalog/band_detail.html"
        )
        self.assertTemplateUsed(
            self.create_response,
            "catalog/band_form.html"
        )
        self.assertTemplateUsed(
            self.delete_response,
            "catalog/band_confirm_delete.html"
        )

    def test_band_list_view_pagination_is_five(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["band_list"]), 5
        )

    def test_band_list_view_lists_all_bands(self):
        response_sec_page = self.client.get(BANDS_LIST_URL + "?page=2")
        bands = Band.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["band_list"]
            ) + list(
                response_sec_page.context["band_list"]
            ), list(bands)
        )

    def test_band_list_view_search(self):
        number_of_bands = 7
        country = Country.objects.create(name="Korea")
        for band_id in range(number_of_bands):
            Band.objects.create(
                name=f"Test_Band {band_id}",
                description=f"Test_Description {band_id}",
                country=country,
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/bands/", {
                    "name": "Test_Band",
                    "page": f"{page_number}"}
            )
            response_list += list(search_result.context["band_list"])
        filter_result = Band.objects.filter(
            name__icontains="Test_Band"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_band_create_view_creates_new_band(self):
        form_data = {
            "name": "Band_Name",
            "description": "Band_Description",
            "country": self.country.id,
            "genres": [self.genre.id],
            "members": [self.user.id]
        }
        self.client.post(BANDS_CREATE_URL, data=form_data)
        new_band = Band.objects.get(
            name=form_data["name"]
        )

        self.assertEqual(new_band.name, form_data["name"])
        self.assertEqual(new_band.description, form_data["description"])

    def test_band_update_view_updates_band(self):
        upd_country = Country.objects.create(name="Egypt")
        upd_genre = Genre.objects.create(name="Soft_Pop")
        upd_instrument = Instrument.objects.create(name="Piano")

        upd_user = get_user_model().objects.create_user(
            username="Upd_Username",
            password="Pazz1234523r3gf",
            instrument=upd_instrument
        )

        form_data = {
            "name": "Upd_Band_Name",
            "description": "Upd_Band_Description",
            "country": upd_country.id,
            "genres": [upd_genre.id],
            "members": [upd_user.id]
        }
        band_id_for_update = Band.objects.get(name="Band 1").id
        self.client.post(reverse(
            "catalog:band-update",
            args=[band_id_for_update]),
            data=form_data
        )
        updated_band = Band.objects.get(
            id=band_id_for_update
        )

        self.assertEqual(updated_band.name, form_data["name"])

    def test_band_delete_view_deletes_band(self):
        band_id_for_delete = Band.objects.get(name="Band 1").id
        self.client.post(reverse(
            "catalog:band-delete",
            args=[band_id_for_delete]
        )
        )

        self.assertEqual(list(Band.objects.filter(name="Band 1")), [])

    def test_band_detail_view_show_all_content(self):
        new_band = Band.objects.create(
            name="Band_D",
            description="description_D",
            country=self.country,
        )
        genre1 = Genre.objects.create(name="Rock")
        genre2 = Genre.objects.create(name="Industrial")
        new_band.genres.add(genre1)
        new_band.genres.add(genre2)
        musician1 = self.user
        musician2 = get_user_model().objects.create_user(
            username="UserMame2",
            password="Pazz12345",
            instrument=self.instrument
        )
        new_band.members.add(musician1)
        new_band.members.add(musician2)

        band_context_response = self.client.get(reverse(
            "catalog:band-detail-view",
            args=[new_band.id])
        ).context["band"]

        self.assertEqual(
            band_context_response.name,
            new_band.name
        )

        self.assertEqual(
            band_context_response.description,
            new_band.description
        )

        self.assertEqual(
            band_context_response.country,
            new_band.country
        )

        self.assertEqual(
            list(band_context_response.genres.all()),
            list(new_band.genres.all())
        )

        self.assertEqual(
            list(band_context_response.members.all()),
            list(new_band.members.all())
        )

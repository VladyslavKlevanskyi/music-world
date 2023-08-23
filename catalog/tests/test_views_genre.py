from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Genre, Instrument

GENRES_LIST_URL = reverse("catalog:genre-list-view")
GENRES_CREATE_URL = reverse("catalog:genre-create")


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Genre-Test")

    def test_login_required_for_genre_list_view(self):
        response = self.client.get(GENRES_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_genre_create(self):
        response = self.client.get(GENRES_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_genre_update(self):
        response = self.client.get(reverse(
            "catalog:genre-update",
            args=[self.genre.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_genre_delete(self):
        response = self.client.get(reverse(
            "catalog:genre-delete",
            args=[self.genre.id])
        )
        self.assertNotEqual(response.status_code, 200)


class GenreViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_genres = 10

        for genre_id in range(number_of_genres):
            Genre.objects.create(name=f"Genre {genre_id}")

    def setUp(self) -> None:
        instrument = Instrument.objects.create(name="Guitar")

        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345",
            instrument=instrument
        )
        self.client.force_login(self.user)

        self.list_response = self.client.get(GENRES_LIST_URL)
        self.create_response = self.client.get(GENRES_CREATE_URL)
        self.update_response = self.client.get(reverse(
            "catalog:genre-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "catalog:genre-delete", args=[1])
        )

    def test_retrieve_genre_list_view(self):
        response = self.client.get(GENRES_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_genre_create(self):
        response = self.client.get(GENRES_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_genre_update(self):
        response = self.client.get(reverse(
            "catalog:genre-update",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_genre_delete(self):
        response = self.client.get(reverse(
            "catalog:genre-delete",
            args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_genre_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/genres/")
        create_view_response = self.client.get("/genres/create/")
        update_view_response = self.client.get("/genres/1/update/")
        delete_view_response = self.client.get("/genres/1/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_genre_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_genre_views_uses_correct_template(self):
        self.assertTemplateUsed(
            self.list_response,
            "catalog/genre_list.html"
        )
        self.assertTemplateUsed(
            self.create_response,
            "catalog/genre_form.html"
        )

        self.assertTemplateUsed(
            self.delete_response,
            "catalog/genre_confirm_delete.html"
        )

    def test_genre_list_view_pagination_is_eight(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["genre_list"]), 8
        )

    def test_genre_list_view_lists_all_genres(self):
        response_sec_page = self.client.get(GENRES_LIST_URL + "?page=2")
        genres = Genre.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["genre_list"]
            ) + list(
                response_sec_page.context["genre_list"]
            ), list(genres)
        )

    def test_genre_list_view_search(self):
        number_of_genres = 10
        for genre_id in range(number_of_genres):
            Genre.objects.create(
                name=f"TestGenre {genre_id}",
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/genres/", {"name": "TestGenre", "page": f"{page_number}"}
            )
            response_list += list(search_result.context["genre_list"])
        filter_result = Genre.objects.filter(
            name__icontains="TestGenre"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_genre_create_view_creates_new_genre(self):
        form_data = {
            "name": "Art Rock",
        }
        self.client.post(reverse("catalog:genre-create"), data=form_data)
        new_genre = Genre.objects.get(name=form_data["name"])

        self.assertEqual(new_genre.name, form_data["name"])

    def test_genre_update_view_updates_genre(self):
        form_data = {
            "name": "Rock",
        }
        genre_id_for_update = Genre.objects.get(name="Genre 1").id
        self.client.post(reverse(
            "catalog:genre-update",
            args=[genre_id_for_update]),
            data=form_data
        )
        updated_genre = Genre.objects.get(
            id=genre_id_for_update
        )

        self.assertEqual(updated_genre.name, form_data["name"])

    def test_genre_delete_view_deletes_genre(self):
        genre_id_for_deletes = Genre.objects.get(name="Genre 1").id
        self.client.post(reverse(
            "catalog:genre-delete",
            args=[genre_id_for_deletes]
        )
        )

        self.assertEqual(list(Genre.objects.filter(name="Genre 1")), [])

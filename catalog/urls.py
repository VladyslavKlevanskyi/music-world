from django.urls import path
from catalog.views import (
    index,
    GenreListView,
    CountryListView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "genres/",
        GenreListView.as_view(),
        name="genre-list-view"
    ),
    path(
        "countries/",
        CountryListView.as_view(),
        name="country-list-view"
    ),
]

app_name = "catalog"

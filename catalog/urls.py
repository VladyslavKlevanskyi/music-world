from django.urls import path
from catalog.views import (
    index,
    GenreListView,
    CountryListView,
    InstrumentListView,
    MusicianListView,
    BandListView
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

    path(
        "instruments/",
        InstrumentListView.as_view(),
        name="instrument-list-view"
    ),

    path(
        "musicians/",
        MusicianListView.as_view(),
        name="musician-list-view"
    ),

    path(
        "bands/",
        BandListView.as_view(),
        name="band-list-view"
    ),
]

app_name = "catalog"

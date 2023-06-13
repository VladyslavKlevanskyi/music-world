from django.urls import path
from catalog.views import (
    index,
    GenreListView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView,
    CountryListView,
    CountryCreateView,
    CountryUpdateView,
    CountryDeleteView,
    InstrumentListView,
    MusicianListView,
    MusicianDetailView,
    BandListView,
    BandDetailView
)

urlpatterns = [
    path("", index, name="index"),

    path(
        "genres/",
        GenreListView.as_view(),
        name="genre-list-view"
    ),
    path(
        "genres/create/",
        GenreCreateView.as_view(),
        name="genre-create"
    ),
    path(
        "genres/<int:pk>/update/",
        GenreUpdateView.as_view(),
        name="genre-update"
    ),
    path(
        "genres/<int:pk>/delete/",
        GenreDeleteView.as_view(),
        name="genre-delete"
    ),

    path(
        "countries/",
        CountryListView.as_view(),
        name="country-list-view"
    ),
    path(
        "countries/create/",
        CountryCreateView.as_view(),
        name="country-create"
    ),
    path(
        "countries/<int:pk>/update/",
        CountryUpdateView.as_view(),
        name="country-update"
    ),
    path(
        "countries/<int:pk>/delete/",
        CountryDeleteView.as_view(),
        name="country-delete"
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
        "musicians/<int:pk>/",
        MusicianDetailView.as_view(),
        name="musician-detail-view"
    ),

    path(
        "bands/",
        BandListView.as_view(),
        name="band-list-view"
    ),
    path(
        "bands/<int:pk>/",
        BandDetailView.as_view(),
        name="band-detail-view"
    ),

]

app_name = "catalog"

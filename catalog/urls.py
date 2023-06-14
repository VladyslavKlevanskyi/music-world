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
    InstrumentCreateView,
    InstrumentUpdateView,
    InstrumentDeleteView,
    MusicianListView,
    MusicianDetailView,
    MusicianCreateView,
    MusicianUpdateView,
    MusicianDeleteView,
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
        "instruments/create/",
        InstrumentCreateView.as_view(),
        name="instrument-create"
    ),
    path(
        "instruments/<int:pk>/update/",
        InstrumentUpdateView.as_view(),
        name="instrument-update"
    ),
    path(
        "instruments/<int:pk>/delete/",
        InstrumentDeleteView.as_view(),
        name="instrument-delete"
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
        "musicians/create/",
        MusicianCreateView.as_view(),
        name="musician-create"
    ),
    path(
        "musicians/<int:pk>/update/",
        MusicianUpdateView.as_view(),
        name="musician-update"
    ),
    path(
        "musicians/<int:pk>/delete/",
        MusicianDeleteView.as_view(),
        name="musician-delete"
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

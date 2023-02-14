from django.shortcuts import render
from django.views import generic

from catalog.models import (
    Band,
    Musician,
    Genre,
    Instrument,
    Country
)


def index(request):
    num_bands = Band.objects.count()
    num_musicians = Musician.objects.count()
    num_genres = Genre.objects.count()
    num_instruments = Instrument.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_bands": num_bands,
        "num_musicians": num_musicians,
        "num_genres": num_genres,
        "num_instruments": num_instruments,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class GenreListView(generic.ListView):
    model = Genre
    template_name = "catalog/genre_list_view.html"


class CountryListView(generic.ListView):
    model = Country
    template_name = "catalog/country_list_view.html"


class InstrumentListView(generic.ListView):
    model = Instrument
    template_name = "catalog/instrument_list_view.html"


class MusicianListView(generic.ListView):
    model = Musician
    template_name = "catalog/musician_list_view.html"


class BandListView(generic.ListView):
    model = Band
    template_name = "catalog/band_list_view.html"

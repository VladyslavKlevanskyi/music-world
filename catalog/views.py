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


class CountryListView(generic.ListView):
    model = Country


class InstrumentListView(generic.ListView):
    model = Instrument


class MusicianListView(generic.ListView):
    model = Musician
    queryset = Musician.objects.all().select_related(
        "instrument"
    ).prefetch_related(
        "bands"
    )


class MusicianDetailView(generic.DetailView):
    model = Musician
    queryset = Musician.objects.all().select_related(
        "instrument"
    ).prefetch_related(
        "bands"
    )


class BandListView(generic.ListView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )


class BandDetailView(generic.DetailView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )

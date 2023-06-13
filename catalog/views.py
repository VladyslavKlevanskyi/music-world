from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import (
    Band,
    Musician,
    Genre,
    Instrument,
    Country
)


@login_required
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


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    paginate_by = 20


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list-view")


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list-view")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("catalog:genre-list-view")


class CountryListView(LoginRequiredMixin, generic.ListView):
    model = Country
    paginate_by = 20


class InstrumentListView(LoginRequiredMixin, generic.ListView):
    model = Instrument
    paginate_by = 20


class MusicianListView(LoginRequiredMixin, generic.ListView):
    model = Musician
    queryset = Musician.objects.all().select_related(
        "instrument"
    ).prefetch_related(
        "bands"
    )
    paginate_by = 8


class MusicianDetailView(LoginRequiredMixin, generic.DetailView):
    model = Musician
    queryset = Musician.objects.all().select_related(
        "instrument"
    ).prefetch_related(
        "bands"
    )


class BandListView(LoginRequiredMixin, generic.ListView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )
    paginate_by = 10


class BandDetailView(LoginRequiredMixin, generic.DetailView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )

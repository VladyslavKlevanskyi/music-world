from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import MusicianCreationForm, BandForm, BandSearchForm
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


class CountryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Country
    fields = "__all__"
    success_url = reverse_lazy("catalog:country-list-view")


class CountryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Country
    fields = "__all__"
    success_url = reverse_lazy("catalog:country-list-view")


class CountryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Country
    success_url = reverse_lazy("catalog:country-list-view")


class InstrumentListView(LoginRequiredMixin, generic.ListView):
    model = Instrument
    paginate_by = 20


class InstrumentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list-view")


class InstrumentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list-view")


class InstrumentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Instrument
    success_url = reverse_lazy("catalog:instrument-list-view")


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


class MusicianCreateView(LoginRequiredMixin, generic.CreateView):
    model = Musician
    form_class = MusicianCreationForm
    success_url = reverse_lazy("catalog:musician-list-view")


class MusicianUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Musician
    form_class = MusicianCreationForm
    success_url = reverse_lazy("catalog:musician-list-view")


class MusicianDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Musician
    success_url = reverse_lazy("catalog:musician-list-view")


class BandListView(LoginRequiredMixin, generic.ListView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BandListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = BandSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class BandDetailView(LoginRequiredMixin, generic.DetailView):
    model = Band
    queryset = Band.objects.all().select_related(
        "country"
    ).prefetch_related(
        "genres"
    )


class BandCreateView(LoginRequiredMixin, generic.CreateView):
    model = Band
    form_class = BandForm
    success_url = reverse_lazy("catalog:band-list-view")


class BandUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Band
    form_class = BandForm
    success_url = reverse_lazy("catalog:band-list-view")


class BandDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Band
    success_url = reverse_lazy("catalog:band-list-view")

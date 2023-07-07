from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import (
    MusicianCreationForm,
    MusicianSearchForm,
    BandForm,
    BandSearchForm,
    GenreSearchForm,
    CountrySearchForm,
    InstrumentSearchForm,
)
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
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = GenreSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Genre.objects.all()

        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


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
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = CountrySearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Country.objects.all()

        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


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
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InstrumentListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = InstrumentSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Instrument.objects.all()

        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


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
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MusicianListView, self).get_context_data(**kwargs)

        searching = self.request.GET.get("musician", "")

        context["search_form"] = MusicianSearchForm(
            initial={"musician": searching}
        )

        return context

    def get_queryset(self):
        queryset = Musician.objects.select_related(
            "instrument"
        ).prefetch_related(
            "bands"
        )

        musician = self.request.GET.get("musician")

        if musician:
            first_name = queryset.filter(first_name__icontains=musician)
            if first_name:
                return first_name

            return queryset.filter(last_name__icontains=musician)

        return queryset


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
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BandListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = BandSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Band.objects.select_related(
            "country"
        ).prefetch_related(
            "genres"
        )

        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import (
    Genre,
    Country,
    Instrument,
    Musician,
    Band
)


@admin.register(Musician)
class MusicianAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("instrument",)
    list_filter = UserAdmin.list_filter + ("instrument",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("instrument",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "instrument",
                    )
                },
            ),
        )
    )


admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Instrument)
admin.site.register(Band)

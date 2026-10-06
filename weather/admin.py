from django.contrib import admin

from .models import Wyszukiwanie


@admin.register(Wyszukiwanie)
class WyszukiwanieAdmin(admin.ModelAdmin):
    list_display = ["miasto", "temperatura", "opis", "uzytkownik", "ip", "data"]
    list_filter = ["uzytkownik", "data"]
    search_fields = ["miasto"]
    
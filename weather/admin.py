from django.contrib import admin

from .models import Miejscowosc, Wyszukiwanie



@admin.register(Wyszukiwanie)
class WyszukiwanieAdmin(admin.ModelAdmin):
    list_display = ["miasto", "temperatura", "opis", "uzytkownik", "ip", "data"]
    list_filter = ["uzytkownik", "data"]
    search_fields = ["miasto"]

@admin.register(Miejscowosc)
class MiejscowoscAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "wojewodztwo", "rodzaj", "sym"]
    list_filter = ["wojewodztwo"]
    search_fields = ["nazwa"]
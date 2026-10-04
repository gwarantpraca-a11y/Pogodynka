import requests
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from .models import Wyszukiwanie


OPISY_POGODY = {
    0: "bezchmurnie",
    1: "przeważnie bezchmurnie",
    2: "częściowe zachmurzenie",
    3: "pochmurno",
    45: "mgła",
    48: "mgła szronowa",
    51: "lekka mżawka",
    53: "mżawka",
    55: "gęsta mżawka",
    61: "lekki deszcz",
    63: "deszcz",
    65: "ulewa",
    71: "lekki śnieg",
    73: "śnieg",
    75: "obfity śnieg",
    80: "przelotny deszcz",
    81: "przelotne opady",
    82: "gwałtowne ulewy",
    95: "burza",
    96: "burza z gradem",
    99: "silna burza z gradem",
}


def index(request):
    miasto = request.GET.get("miasto", "Zielona Góra")

    try:
        # Telefon 1: gdzie leży to miasto?
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": miasto, "count": 1, "language": "pl"},
            timeout=10,
        )
        geo.raise_for_status()
        wyniki = geo.json().get("results")

        if not wyniki:
            kontekst = {"miasto": miasto, "blad": "Nie znalazłem takiego miasta"}
            return render(request, "weather/index.html", kontekst)

        miejsce = wyniki[0]

        # Telefon 2: jaka tam jest pogoda?
        pogoda = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": miejsce["latitude"],
                "longitude": miejsce["longitude"],
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            },
            timeout=10,
        )
        pogoda.raise_for_status()
        teraz = pogoda.json()["current"]

    except requests.RequestException:
        kontekst = {"miasto": miasto, "blad": "Brak połączenia z serwisem pogodowym"}
        return render(request, "weather/index.html", kontekst)

    opis = OPISY_POGODY.get(teraz["weather_code"], "nieznana pogoda")

    if "miasto" in request.GET:
        Wyszukiwanie.objects.create(
            miasto=miejsce["name"],
            temperatura=teraz["temperature_2m"],
            opis=opis,
            ip=request.META.get("REMOTE_ADDR"),
            uzytkownik=request.user if request.user.is_authenticated else None,
        )

    kontekst = {
        "miasto": miejsce["name"],
        "kraj": miejsce.get("country", ""),
        "temperatura": teraz["temperature_2m"],
        "wilgotnosc": teraz["relative_humidity_2m"],
        "wiatr": teraz["wind_speed_10m"],
        "opis": opis,
    }
    return render(request, "weather/index.html", kontekst)

def rejestracja(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            nowy = form.save()
            login(request, nowy)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "registration/rejestracja.html", {"form": form})

def about(request):
    return HttpResponse("Aplikacja do zmiany pogody .")
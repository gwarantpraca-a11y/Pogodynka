import csv

from django.core.management.base import BaseCommand

from weather.models import Miejscowosc

WOJEWODZTWA = {
    "02": "dolnośląskie",
    "04": "kujawsko-pomorskie",
    "06": "lubelskie",
    "08": "lubuskie",
    "10": "łódzkie",
    "12": "małopolskie",
    "14": "mazowieckie",
    "16": "opolskie",
    "18": "podkarpackie",
    "20": "podlaskie",
    "22": "pomorskie",
    "24": "śląskie",
    "26": "świętokrzyskie",
    "28": "warmińsko-mazurskie",
    "30": "wielkopolskie",
    "32": "zachodniopomorskie",
}


class Command(BaseCommand):
    help = "Importuje miejscowości z pliku SIMC (GUS)"

    def add_arguments(self, parser):
        parser.add_argument("plik", help="ścieżka do pliku CSV z SIMC")

    def handle(self, *args, **options):
        miejscowosci = []

        with open(options["plik"], encoding="utf-8-sig", newline="") as plik:
            for wiersz in csv.DictReader(plik, delimiter=";"):
                if wiersz["SYM"] != wiersz["SYMPOD"]:
                    continue
                miejscowosci.append(
                    Miejscowosc(
                        sym=wiersz["SYM"],
                        nazwa=wiersz["NAZWA"],
                        wojewodztwo=WOJEWODZTWA.get(wiersz["WOJ"], ""),
                        rodzaj=wiersz["RM"],
                    )
                )

        Miejscowosc.objects.all().delete()
        Miejscowosc.objects.bulk_create(miejscowosci, batch_size=5000)

        self.stdout.write(
            self.style.SUCCESS(f"Zaimportowano {len(miejscowosci)} miejscowości")
        )
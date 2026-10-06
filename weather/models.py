from django.conf import settings
from django.db import models
from django.utils import timezone


class Wyszukiwanie(models.Model):
    miasto = models.CharField(max_length=100)
    temperatura = models.FloatField()
    opis = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(null=True, blank=True)
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    data = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "wyszukiwanie"
        verbose_name_plural = "wyszukiwania"
        ordering = ["-data"]
class Miejscowosc(models.Model):
    sym = models.CharField(max_length=7, unique=True)
    nazwa = models.CharField(max_length=100, db_index=True)
    wojewodztwo = models.CharField(max_length=30)
    rodzaj = models.CharField(max_length=2)

    class Meta:
        verbose_name = "miejscowość"
        verbose_name_plural = "miejscowości"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.nazwa} ({self.wojewodztwo})"
        
    
    
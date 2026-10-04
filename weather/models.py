from django.conf import settings
from django.db import models


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

        
    def __str__(self):
        return f"{self.miasto} ({self.data:%Y-%m-%d %H:%M})"
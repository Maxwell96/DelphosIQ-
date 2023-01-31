from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=150, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(_("Sector"), max_length=150, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    symbol = models.CharField(_("Currency"), max_length=3, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.symbol


class Loan(models.Model):
    date = models.DateField(_("Signature date"), auto_now_add=False, auto_now=False, blank=False)
    title = models.CharField(max_length=250)
    country = models.ForeignKey(Country, blank=False, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, blank=False, on_delete=models.CASCADE)
    amount = models.IntegerField(_("Signed amount"), blank=False)
    currency = models.ForeignKey(Currency, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

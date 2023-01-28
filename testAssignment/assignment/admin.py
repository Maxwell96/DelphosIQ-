from django.contrib import admin

from .models import Sector, Loan, Country

# Register your models here.
admin.site.register(Country)
admin.site.register(Sector)
admin.site.register(Loan)

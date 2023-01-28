from django.urls import path
from .views import LoanView, CountryView, SectorView

urlpatterns = [
    path('api/loans/', LoanView.as_view(), name='loan_list'),
    path('api/countries/', CountryView.as_view(), name='countries'),
    path('api/sectors/', SectorView.as_view(), name='sectors'),
]

from rest_framework.generics import ListAPIView

from .models import Loan, Country, Sector
from .serializer import LoanSerializer, CountrySerializer, SectorSerializer


class LoanView(ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CountryView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SectorView(ListAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

from rest_framework import serializers

from .models import Loan, Country, Sector, Currency


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    sector = SectorSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Loan
        fields = "__all__"

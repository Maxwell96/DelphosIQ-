from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import time
from datetime import datetime

from django.db.models import Sum

from ...models import Currency, Country, Loan, Sector

from ...utils import excel_generator


class Command(BaseCommand):
    help = "Runs a Selenium script to scrape data from a website"

    def handle(self, *args, **options):
        # Website URL
        url = "https://www.eib.org/en/projects/loans/index.htm"

        # Selenium to open website with chrome
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)

        # Handle Accept Cookies popup
        # driver.find_element(By.ID, "accept_cookies_footer").click()

        # Change the loan table to 100 rows per page
        select_element = Select(driver.find_element(By.XPATH, '//select[@id="show-entries"]'))
        select_element.select_by_value("100")
        time.sleep(10)

        # Get loan table from the website
        loan_table = driver.find_elements(By.TAG_NAME, "article")

        dates = []
        titles = []
        countries = []
        sectors = []
        amounts = []

        for row in loan_table[1:-1]:
            # Convert String to List
            data = row.text.split("\n")
            # Create a Country object
            country, _ = Country.objects.get_or_create(name=data[2])
            # Create a Sector object
            sector, _ = Sector.objects.get_or_create(name=data[3])
            # Create a Currency object
            currency, _ = Currency.objects.get_or_create(symbol=data[4][0])
            # Create a Loan object
            Loan.objects.create(date=datetime.strptime(data[0], "%d %B %Y").date().strftime("%Y-%m-%d"),
                                title=data[1], country=country, sector=sector,
                                amount=int(data[4][1:].replace(",", "")), currency=currency)

            dates.append(data[0])
            titles.append(data[1])
            countries.append(data[2])
            sectors.append(data[3])
            amounts.append(data[4])

        # Categorize loans and find sum
        loans_by_year = Loan.objects.values("date__year").annotate(Sum("amount"))
        loans_by_country = Loan.objects.values("country__name").annotate(Sum("amount"))
        loans_by_sector = Loan.objects.values("sector__name").annotate(Sum("amount"))

        # Preparing sheet data
        sheet_data = [dates, titles, countries, sectors, amounts]
        headers = ["Signature date", "Title", "Country", "Sectors", "Signed Amount"]

        # Preparing chart data
        chart_data = [loans_by_year, loans_by_country, loans_by_sector]
        chart_data_headers = [["date__year", "amount__sum"], ["country__name", "amount__sum"],
                              ["sector__name", "amount__sum"]]

        excel_generator.generate_workbook(workbook_name="loan_data.xlsx", sheet_data=sheet_data,
                                          sheet_data_headers=headers, chart_data=chart_data,
                                          chart_data_headers=chart_data_headers)


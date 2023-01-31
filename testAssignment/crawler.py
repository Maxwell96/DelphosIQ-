from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from django.db.models import Sum

import time
from datetime import datetime

import xlsxwriter

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testAssignment.settings")
django.setup()

from assignment.models import Country, Sector, Loan, Currency

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
currencies = []

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

# Creating workbook
workbook = xlsxwriter.Workbook("loan_data.xlsx")

# Creating worksheets
data_sheet = workbook.add_worksheet("Data sheet")

title_format = workbook.add_format()
title_format.set_bold()
title_format.set_font_size(12)
title_format.set_align('center')

entries_format = workbook.add_format()
entries_format.set_align('center')

# Adding headers
header_list = ["Signature date", "Title", "Country", "Sectors", "Signed Amount"]
for i, header in enumerate(header_list):
    data_sheet.write(0, i, str(header).upper(), title_format)

# Adding entries
data = [dates,
        titles,
        countries,
        sectors,
        amounts]
for j, row_data in enumerate(data):
    for i, entry in enumerate(row_data):
        data_sheet.write(i + 1, j, entry, entries_format)

data_sheet.autofit()

# Creating Chart Sheet
chart_sheet = workbook.add_worksheet('Chartsheet')

# Categorize loans and find sum
loans_by_year = Loan.objects.values("date__year").annotate(Sum("amount"))
loans_by_country = Loan.objects.values("country__name").annotate(Sum("amount"))
loans_by_sector = Loan.objects.values("sector__name").annotate(Sum("amount"))

# Creating dummy sheets for the charts
dummy_sheet = workbook.add_worksheet("Dummysheet")
start_row = 0
for entry in loans_by_year:
    dummy_sheet.write(start_row, 0, entry["date__year"])
    dummy_sheet.write(start_row, 1, entry["amount__sum"])
    start_row += 1

start_row = 0
for entry in loans_by_country:
    dummy_sheet.write(start_row, 2, entry["country__name"])
    dummy_sheet.write(start_row, 3, entry["amount__sum"])
    start_row += 1

start_row = 0
for entry in loans_by_sector:
    dummy_sheet.write(start_row, 4, entry["sector__name"])
    dummy_sheet.write(start_row, 5, entry["amount__sum"])
    start_row += 1

# Creating a chat object
chart = workbook.add_chart({"type": "column"})

# Creating dynamic data to be used for the chart series as defined names
chart_x_label = f'=IF(Chartsheet!$A$1="By Year",\
            Dummysheet!$B$1:$B${len(loans_by_year) + 1},\
            IF(Chartsheet!$A$1="By Country",\
            Dummysheet!$D$1:$D${len(loans_by_country) + 1},\
            Dummysheet!$F$1:$F${len(loans_by_sector) + 1}\
        )\
    )'

chart_y_label = f'=IF(Chartsheet!$A$1="By Year",\
            Dummysheet!$A$1:$A${len(loans_by_year) + 1},\
            IF(Chartsheet!$A$1="By Country",\
            Dummysheet!$C$1:$C${len(loans_by_country) + 1},\
            Dummysheet!$E$1:$E${len(loans_by_sector) + 1}\
        )\
    )'

# Creating named ranges for the data in each sheet
workbook.define_name("chart_series", chart_y_label)
workbook.define_name("chart_labels", chart_x_label)

# Adding a drop-down list for selecting the data to display
chart_sheet.data_validation("A1", {"validate": "list",
                                   "source": ["By Year", "By Country", "By Sector"],
                                   "input_title": "Select Data",
                                   "input_message": "Select data to display in chart"})

# Adding dropdown format
dropdown_format = workbook.add_format(
        {"bg_color": "black", "bold": True, "align": "center", "font_color": "white"}
    )

# Setting default value to the cell
chart_sheet.write("A1", "By Year", dropdown_format)

# Configuring the data series for the chart
chart.add_series({
    'values': '=Dummysheet!chart_labels',
    'categories': '=Dummysheet!chart_series',
    'name': 'Selected Data',
})

# Formatting chart
chart.set_size({"width": 720, "height": 350})
chart.set_style(8)
chart.set_legend({"none": True})

# Inserting the charts into the chart sheet
chart_sheet.insert_chart("E3", chart)

# Hiding dummy sheet
dummy_sheet.hide()

workbook.close()

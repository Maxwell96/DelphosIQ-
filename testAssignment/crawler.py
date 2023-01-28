from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import time
from datetime import datetime

import xlsxwriter

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testAssignment.settings")
django.setup()

from assignment.models import Country, Sector, Loan

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
    Loan.objects.create(date=datetime.strptime(data[0], "%d %B %Y").date().strftime("%Y-%m-%d"),
                        title=data[1], country=country, sector=sector,
                        amount=int(data[4][1:].replace(",", "")), currency=data[4][0])

    dates.append(data[0])
    titles.append(data[1])
    countries.append(data[2])
    sectors.append(data[3])
    amounts.append(data[4])

# Creating workbook
workbook = xlsxwriter.Workbook("loan_data.xlsx")

# Creating worksheets
data_sheet = workbook.add_worksheet("Data sheet")
chart_sheet = workbook.add_worksheet("Chart sheet")

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
for i, entry in enumerate(dates):
    data_sheet.write(i + 1, 0, entry, entries_format)

for i, entry in enumerate(titles):
    data_sheet.write(i + 1, 1, entry, entries_format)

for i, entry in enumerate(countries):
    data_sheet.write(i + 1, 2, entry, entries_format)

for i, entry in enumerate(sectors):
    data_sheet.write(i + 1, 3, entry, entries_format)

for i, entry in enumerate(amounts):
    data_sheet.write(i + 1, 4, entry, entries_format)

data_sheet.autofit()



workbook.close()

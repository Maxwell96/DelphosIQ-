from selenium import webdriver

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
import time

from datetime import datetime

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

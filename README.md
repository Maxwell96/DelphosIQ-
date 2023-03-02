# Django Selenium Project
A project that uses a crawler to scrape data from a dynamic website. The data is published to necessary API endpoints and an excel workbook is generated with a data sheet and chart sheet. 

## Prerequisites

- Python 3.x
- Django 4.x

## Installation

1. Clone the repository: git clone https://github.com/Maxwell96/DelphosIQ-.git
2. Change into the project directory: cd testAssignment
3. Install dependencies: pip install -r requirements.txt
4. Run migrations: python manage.py migrate

## Running the Project

1. Run crawler: python manage.py crawler 
2. Start the development server: python manage.py runserver
3. Open your browser and navigate to http://localhost:8000

### Built With

- Django
- Python
- Selenium
- Xlsxwriter

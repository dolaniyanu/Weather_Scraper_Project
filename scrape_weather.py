### PROJECT
### weather_scraper.py
### NAME  : DANIEL OLANIYANU
### CLASS : ADEV-3005 (261248)
### DATE  : 2025-03-28

"""
scrape_weather.py

The WeatherScraper class is made to scrape daily weather data, extracting temperature data 
from Canada's climate website; (maximum, minimum, and mean) for each day of a month. 
The scraper starts from the current month and year and proceeds backward until there is no more data.
"""

import urllib.request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
import datetime
import logging

# Configure logging early
logging.basicConfig(
    filename='weather_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WeatherScraper(HTMLParser):
    """
    A class that extends HTMLParser to scrape daily temperature data (max, min, mean)
    from a provided URL, which points to a weather data page for a specific month and year.
    The scraper navigates the table of daily data, extracting values for each day.

    Attributes:
        web_url (str): The weather daily data URL with placeholders for year and month.
        in_data_table (bool): Checks if the parser is inside the data table.
        in_tbody (bool): Checks if the parser is inside the table body.
        current_row (list): Stores the current row of data being processed.
        daily_values (list): List to store daily weather data (day, max, min, mean).
        capture_data (bool): Flag indicating whether data should be captured for a cell.
        cell_data (list): Stores data for the current cell being processed.
    """

    def __init__(self, web_url):
        """
        Initializes the WeatherScraper with the provided web URL.

        Args:
            web_url (str): The URL template used for scraping weather data, 
                           with placeholders for year and month.
        """
        super().__init__()
        self.web_url = web_url 
        self.in_data_table = False
        self.in_tbody = False 
        self.current_row = []  # Stores the data of the current row being parsed.
        self.daily_values = [] 
        self.capture_data = False 
        self.cell_data = [] 

    def handle_starttag(self, tag, attrs):
        """
        Handles the start tag of the HTML elements during parsing.
        Detects when the parser enters the data table and captures relevant data.

        Args:
            tag (str): The tag name.
            attrs (list): A list of tuples containing tag attributes and values.
        """
        if tag.lower() == 'table':
            for attr_name, attr_value in attrs:
                if attr_name.lower() == "class" and "table" in attr_value:
                    self.in_data_table = True  # Parser is inside the table element.
        if self.in_data_table:
            if tag.lower() == 'tbody':
                self.in_tbody = True  # Parser is inside the tbody element.
            if tag.lower() in ('td', 'th', 'abbr'):
                self.capture_data = True  # Indicates that the parser should capture cell data.
                if not self.cell_data:
                    self.cell_data = []  # Temporarily stores data of a new cell in the table.

    def handle_data(self, data):
        """
        Handles the text data inside tags during parsing.
        Captures the content of cells within the data table.

        Args:
            data (str): The text data inside the HTML element.
        """
        if self.capture_data and self.in_data_table and self.in_tbody:
            self.cell_data.append(data.strip())

    def handle_endtag(self, tag):
        """
        Handles the end tag of the HTML elements during parsing.
        Finalizes the data captured for a cell and processes the row data.

        Args:
            tag (str): The tag name.
        """
        if self.capture_data and tag.lower() in ('td', 'th'):
            self.capture_data = False  # Recognizes parser should stop

            # Join captured data to the current row.
            cell_text = " ".join(self.cell_data).strip()
            self.current_row.append(cell_text)  # Add cell to the current row.
            self.cell_data = []  # Reset the cell data.

        if tag.lower() == 'tr' and self.in_data_table and self.in_tbody:
            if len(self.current_row) >= 4:
                day_str = self.current_row[0]
                max_str = self.current_row[1]
                min_str = self.current_row[2]
                mean_str = self.current_row[3]
                if day_str.isdigit():  # Validates Date.
                    try:
                        max_val = float(max_str)
                        min_val = float(min_str)
                        mean_val = float(mean_str)
                        self.daily_values.append((int(day_str), max_val, min_val, mean_val)) 
                    except ValueError:
                        pass  # Skip rows with invalid data
            self.current_row = []  # Reset the current row.

        if tag.lower() == 'tbody' and self.in_data_table:
            self.in_tbody = False
        if tag.lower() == 'table' and self.in_data_table:
            self.in_data_table = False

    def fetch_month_data(self, year, month):
        """
        Fetches and parses weather data for a specific month and year.

        Args:
            year (int): The year for which the weather data is fetched.
            month (int): The month for which the weather data is fetched.

        Returns:
            list: A list of tuples containing daily data in the format (day, max, min, mean).
        """
        url = self.web_url.format(year=year, month=month)  # Formats the URL with year and month.
        try:
            with urllib.request.urlopen(url) as response:
                html_bytes = response.read()
                html_text = html_bytes.decode('utf-8')
        except (HTTPError, URLError) as e:
            print(f"Failed to retrieve {url}: {e}")
            return []

        if "We're sorry we were unable to satisfy your request." in html_text:
            return []

        self.reset()  # Reset the parser state.
        self.daily_values = []  # Clear any existing daily values.
        self.feed(html_text)
        return self.daily_values  # Return the parsed daily data.

    def scrape(self):
        """
        Starts the scraping process from the current date and proceeds backward month by month,
        collecting weather data until no earlier real data is available.
        Detects when data becomes frozen and stops BEFORE scraping duplicate months.
        """
        today = datetime.date.today()
        current_year = today.year
        current_month = today.month

        result = {}
        last_daily_values = None

        while True:
            print(f"\nScraping data for: {current_year}-{current_month:02d}")

            daily_values = self.fetch_month_data(current_year, current_month)

            if not daily_values:
                print(f"No data found for {current_year}-{current_month:02d}, moving to previous month...")
            else:
                if last_daily_values == daily_values:
                    print(f"\nDuplicate monthly data detected at {current_year}-{current_month:02d}! Stopping scraper BEFORE saving.")
                    break

                month_key = f"{current_year}-{current_month:02d}"
                result[month_key] = daily_values

                for day, max_val, min_val, mean_val in daily_values:
                    date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                    print(f"{date_str}: Max={max_val} Min={min_val} Mean={mean_val}")

                last_daily_values = daily_values

            if current_month == 1:
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1

            if current_year < 1900:
                print("Hard stop: Reached year before 1900. Stopping to prevent infinite loop.")
                break

        return result


if __name__ == "__main__":
    """
    Initializes the scraper with a given URL, starts the scraping process.
    Provides a string representation of the scraped data.
    """
    # Define the URL with placeholders for year and month
    WEB_URL = (
        "https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
        "StationID=27174&Year={year}&Month={month}&Day=1&timeframe=2"
    )

    # Create a new instance of the WeatherScraper class with the defined URL
    scraper = WeatherScraper(WEB_URL)

    # Scraping begins
    scraper.scrape()

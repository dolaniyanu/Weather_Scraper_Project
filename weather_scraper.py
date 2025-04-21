### PROJECT
### weather_scraper.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-03-28

import urllib.request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
import datetime

"""
The WeatherScraper class is made to scrape daily weather data, extracting temperature data 
from Canada's climate website; (maximum, minimum, and mean) for each day of a month. 
The scraper starts from the current month and year and proceeds backward until it reaches May 2018.
"""

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
        self.current_row = [] # Stores the data of the current row being parsed.
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
        # Checks if the current tag is a table
        if tag.lower() == 'table':
            for attr_name, attr_value in attrs:
                if attr_name.lower() == "class" and "table" in attr_value:
                    self.in_data_table = True # Parser is inside the table element.
        # Checks for the table body (tbody)
        if self.in_data_table:
            if tag.lower() == 'tbody':
                self.in_tbody = True # Parser is inside the tbody element.

            # Checks for the table data (td), table header (th)
            if tag.lower() in ('td', 'th'):
                self.capture_data = True # Indicates that the parser should capture cell data.
                self.cell_data = [] # Temporarily stores data of a new cell in the table.

    def handle_data(self, data):
        """
        Handles the text data inside tags during parsing.
        Captures the content of cells within the data table.
        
        Args:
            data (str): The text data inside the HTML element.
        """
        # Captures data when inside the table body and the parser should capture cell data.
        if self.capture_data and self.in_data_table and self.in_tbody:
            self.cell_data.append(data.strip())

    def handle_endtag(self, tag):
        """
        Handles the end tag of the HTML elements during parsing.
        Finalizes the data captured for a cell and processes the row data.
        
        Args:
            tag (str): The tag name.
        """
        # When the end of a table cell is reached, parser stop capturing.
        if self.capture_data and tag.lower() in ('td', 'th'):
            self.capture_data = False # Reconizes parser should stop

            # Join captured data to the current row.
            cell_text = " ".join(self.cell_data).strip()
            self.current_row.append(cell_text)# Add cell to the current row.
            self.cell_data = [] # Reset the cell data.

        # Handle the collected row data
        if tag.lower() == 'tr' and self.in_data_table and self.in_tbody:
            if len(self.current_row) >= 4:
                # Extract data for day, max, min, and mean values.
                day_str  = self.current_row[0]
                max_str  = self.current_row[1]
                min_str  = self.current_row[2]
                mean_str = self.current_row[3]
                if day_str.isdigit():  # Validates Date.
                    try:
                        # Convert the strings to float and append the values as a tuple.
                        max_val  = float(max_str)
                        min_val  = float(min_str)
                        mean_val = float(mean_str)
                        self.daily_values.append((int(day_str), max_val, min_val, mean_val)) 
                    except ValueError:
                        pass # Skip rows with invalid data.

            self.current_row = [] # Resets the current row.

        # Resets the booleans used to help navigate the parser on the HTML.
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
        url = self.web_url.format(year=year, month=month)# Formats the URL with year and month.
        try:
            # Gets and then decodes the HTML content.
            with urllib.request.urlopen(url) as response:
                html_bytes = response.read() 
                html_text = html_bytes.decode('utf-8')
        except (HTTPError, URLError) as e:
            print(f"Failed to retrieve {url}: {e}")
            return []

        if "We're sorry we were unable to satisfy your request." in html_text:
            return []

        self.reset() # Reset the parser state.
        self.daily_values = [] # Clear any existing daily values.
        self.feed(html_text)
        return self.daily_values # Return the parsed daily data.

    def scrape(self):
        """
        Starts the scraping process from the current date and proceeds backward month by month,
        collecting weather data until May 2018 is reached. 
        Prints out the daily weather data for each month.
        """
        today = datetime.date.today()
        current_year = today.year
        current_month = today.month

        hardCap_year = 1960 # The hard-cap year (1960), where scrape data ought to stop on an error.
        softCap_year = 2018 # The soft-cap year (2018), where scrape data ought to stop.
        softCap_month = 5 # The soft-cap month (May), where scrape data ought to stop.
        result = {} # Initializes an empty dictionary to store all the month to month weather data.

        while True:
            print(f"\nScraping data for: {current_year}-{current_month:02d}")
            # Fetches data from the current month.
            daily_values = self.fetch_month_data(current_year, current_month)

            for day, max_val, min_val, mean_val in daily_values:
                # Prints string representation out of scraped data for each day.
                date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                print(f"{date_str}: Max={max_val} Min={min_val} Mean={mean_val}")

            month_value = f"{current_year}-{current_month:02d}" # Format the current year and month as a string.
            result[month_value] = daily_values # Stores the list of daily values of a specific month in the dictionary using the formatted month value.

            if current_year == softCap_year and current_month == softCap_month:
                print("\nReached URL stop date: May 2018. Stopping scraping.")
                break # A defined soft-cap : when scrape data reaches May 2018

            # Move process to the previous month
            if current_month == 1:
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1

            # A defined hard-cap of how far back code can scrape on an error
            if current_year < hardCap_year:
                print("Stopping due to redundancy.")
                break

        return result # Returns a potentially filled dictionary.
if __name__ == "__main__":
    """
    Initializes the scraper with a given URL, starts the scraping process.
    Provides a string representation of the scraped data.
    """

    # Define the URL with placeholders for year and month.
    web_url = (
        "https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
        "StationID=27174&Year={year}&Month={month}&Day=1&timeframe=2"
    )

    # Create a new instance of the WeatherScraper class with the defined URL.
    scraper = WeatherScraper(web_url)

    # Scraping begins.
    scraper.scrape()

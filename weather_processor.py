### PROJECT
### weather_processor.py
### NAME  : DANIEL OLANIYANU
### CLASS : ADEV-3005 (261248)
### DATE  : 2025-04-20

"""
weather_processor.py

Provides the WeatherProcessor class which allows users to
download Winnipeg weather data, save it to a database, and generate 
visualizations like box plots and line plots.
"""

import logging
import datetime
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor:
    """
    A class that is responsible for the visualization of scraping and data plots for the user.
    """

    def __init__(self):
        """
        Initializes the WeatherProcessor object.
        """
        try:
            self.db_name = "weather.sqlite"
            self.scraper = WeatherScraper(
                "https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
                "StationID=27174&Year={year}&Month={month}&Day=1&timeframe=2"
            )
            self.plotter = PlotOperations(self.db_name)
        except Exception as e:
            logging.error('Error in __init__: %s', e)
            raise

    def display_menu(self):
        """
        Displays the user menu and handles user input for database and plot operations.
        """
        try:
            while True:
                print("\nWinnipeg Weather Data Processor")
                print("1. Download all weather data")
                print("2. Generate the Monthly Temprature Distribution (Box plot)")
                print("3. Generate the Current Month's Daily Mean Temprature (Line plot)")
                print("4. Exit")

                choice = input("Select an option (1-4): ")

                if choice == '1':
                    self.download_all_data()
                elif choice == '2':
                    self.generate_boxplot()
                elif choice == '3':
                    self.generate_lineplot()
                elif choice == '4':
                    print("Exiting Weather Processor.")
                    break
                else:
                    print("Invalid input. Please try again.")
        except Exception as e:
            logging.error('Error in display_menu: %s', e)
            raise

    def download_all_data(self):
        """
        Starts the scraping and database saving of all weather data.
        """
        try:
            DBOperations.initialize_db()
            print("Downloading the complete weather dataset...")
            data = self.scraper.scrape()
            if data:
                DBOperations.save_data(data)
                print("Data saved to database.")
            else:
                print("No data was downloaded.")
        except Exception as e:
            logging.error('Error in download_all_data: %s', e)
            raise

    def generate_boxplot(self):
        """
        Generates a boxplot based on a user-defined year range.
        """
        try:
            earliest_year = 1996
            current_year = datetime.datetime.now().year
            print(f"\nAvailable data range: {earliest_year} to {current_year}")

            first_year = int(input("Enter the start year (e.g., 2018): "))
            if first_year > current_year:
                print(f"Starting year cannot be greater than {current_year}. Please try again.")
                return
            if first_year < earliest_year:
                print(f"Starting year cannot be less than {earliest_year}. Please try again.")
                return

            last_year = int(input("Enter the end year (e.g., 2023): "))
            if last_year > current_year:
                print(f"Ending year cannot be greater than {current_year}. Please try again.")
                return
            if last_year < earliest_year:
                print(f"Ending year cannot be less than {earliest_year}. Please try again.")
                return

            if first_year > last_year:
                print(f"Starting year cannot be farther than the last user input {last_year}. Please try again.")
                return
            if last_year < first_year:
                print(f"Ending year cannot be earlier than the first user input {first_year}. Please try again.")
                return

            self.plotter.plot_boxplot(first_year, last_year)

        except ValueError:
            print("Invalid year input. Please enter numeric values.")
        except Exception as e:
            logging.error('Error in generate_boxplot: %s', e)
            raise

    def generate_lineplot(self):
        """
        Generates a line plot for a user-specified year and month.
        """
        try:
            earliest_year = 1996
            current_year = datetime.datetime.now().year
            print(f"\nAvailable data range: {earliest_year} to {current_year}")

            year = int(input("Enter the year (e.g., 2023): "))
            if year > current_year:
                print(f"Year input cannot be greater than {current_year}. Please try again.")
                return
            if year < earliest_year:
                print(f"Year input cannot be less than {earliest_year}. Please try again.")
                return

            month = int(input("Enter the month (1-12): "))
            if 1 <= month <= 12:
                self.plotter.plot_lineplot(year, month)
            else:
                print("Invalid month. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            logging.error('Error in generate_lineplot: %s', e)
            raise


if __name__ == "__main__":
    processor = WeatherProcessor()
    processor.display_menu()

# Logging
logging.basicConfig(
    filename='weather_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

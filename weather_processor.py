### PROJECT
### weather_processor.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-20

import logging
from weather_scraper import WeatherScraper
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
            logging.error(f'Error in __init__: {e}')
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
            logging.error(f'Error in display_menu: {e}')
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
            logging.error(f'Error in download_all_data: {e}')
            raise

    def generate_boxplot(self):
        """
        Generates a boxplot of monthly temperature distribution.
        """
        try:
            self.plotter.plot_boxplot()
        except Exception as e:
            logging.error(f'Error in generate_boxplot: {e}')
            raise

    def generate_lineplot(self):
        """
        Generates a line plot portraying the daily mean temperatures for the current month.
        """
        try:
            self.plotter.plot_lineplot()
        except Exception as e:
            logging.error(f'Error in generate_lineplot: {e}')
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
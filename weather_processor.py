### PROJECT
### weather_processor.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-20

from weather_scraper import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations
import datetime

class WeatherProcessor:
    def __init__(self):
        self.db_name = "weather.sqlite"
        self.scraper = WeatherScraper(
            "https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
            "StationID=27174&Year={year}&Month={month}&Day=1&timeframe=2"
        )
        self.plotter = PlotOperations(self.db_name)

    def display_menu(self):
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

    def download_all_data(self):
        DBOperations.initialize_db()
        print("Downloading the complete weather dataset...")
        data = self.scraper.scrape()
        if data:
            DBOperations.save_data(data)
            print("Data saved to database.")
        else:
            print("No data was downloaded.")

    def generate_boxplot(self):
        self.plotter.plot_boxplot()

    def generate_lineplot(self):
        self.plotter.plot_lineplot()

if __name__ == "__main__":
    processor = WeatherProcessor()
    processor.display_menu()
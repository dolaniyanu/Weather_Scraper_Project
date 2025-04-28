### PROJECT
### plot_operations.py
### NAME  : DANIEL OLANIYANU
### CLASS : ADEV-3005 (261248)
### DATE  : 2025-04-20

"""
plot_operations.py

Handles the visualization of weather data from the SQLite database.
Provides functionality to create boxplots and line plots of temperature data.
"""

import sqlite3
from collections import defaultdict
import datetime
import logging
import matplotlib.pyplot as plt

class PlotOperations:
    """
    A class that is responsible for generating visualizations of weather data.
    """

    def __init__(self, db_name="weather.sqlite"):
        """
        Initializes PlotOperations with the target SQLite database.
        """
        self.db_name = db_name

    def _fetch_data(self):
        """
        Fetches the average temperatures from the database.

        Returns:
            list: List of tuples (sample_date, avg_temp)
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sample_date, avg_temp FROM weather")
                return cursor.fetchall()
        except Exception as e:
            logging.error('Error in _fetch_data: %s', e)
            raise

    def prepare_data(self):
        """
        Prepares monthly and daily average temperature data grouped by date.

        Returns:
            tuple: (monthly_data: dict, daily_data: dict)
        """
        try:
            rows = self._fetch_data()
            monthly_data = defaultdict(list)
            daily_data = defaultdict(list)

            for sample_date, avg_temp in rows:
                # Convert the string date into a datetime object
                date_block = datetime.datetime.strptime(sample_date, "%Y-%m-%d")
                month = date_block.month
                year_month = date_block.strftime("%Y-%m")

                # Group temperatures by month and by specific year-month combinations
                monthly_data[month].append(avg_temp)
                daily_data[year_month].append((date_block.day, avg_temp))

            return monthly_data, daily_data
        except Exception as e:
            logging.error('Error in prepare_data: %s', e)
            raise

    def plot_boxplot(self, start_year, end_year):
        """
        Plots a boxplot of monthly mean temperature distributions for a given year range.

        Args:
            start_year (int): The starting year.
            end_year (int): The ending year.
        """
        try:
            rows = self._fetch_data()

            # Filter rows by start and end year
            filtered_rows = []
            for sample_date, avg_temp in rows:
                if avg_temp is not None:
                    date_block = datetime.datetime.strptime(sample_date, "%Y-%m-%d")
                    if start_year <= date_block.year <= end_year:
                        filtered_rows.append((date_block, avg_temp))

            # Group by month
            monthly_data = defaultdict(list)
            for date_block, avg_temp in filtered_rows:
                monthly_data[date_block.month].append(avg_temp)

            # Plot
            plt.figure(figsize=(12, 6))
            plt.boxplot(
                [monthly_data[m] for m in range(1, 13)],
                labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            )
            plt.title(f"Monthly Temperature Distribution ({start_year}-{end_year})")
            plt.xlabel("Month")
            plt.ylabel("Mean Temperature (°C)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            logging.error('Error in plot_boxplot: %s', e)
            raise

    def plot_lineplot(self, year, month):
        """
        Plots a line graph of daily mean temperatures for the specified month and year.

        Args:
            year (int): The year to plot.
            month (int): The month to plot.
        """
        try:
            _, daily_data = self.prepare_data()
            year_month = f"{year}-{month:02d}"

            if year_month not in daily_data:
                print(f"No data available for {year_month}.")
                return

            # Sort by day
            daily_temps = sorted(daily_data[year_month], key=lambda x: x[0])
            days = [day for day, temp in daily_temps]
            temps = [temp for day, temp in daily_temps]

            plt.figure(figsize=(12, 6))

            # Line + markers on each day
            plt.plot(days, temps, marker='o', linestyle='-')

            plt.title(f"Daily Mean Temperature: {year_month}")
            plt.xlabel("Day")
            plt.ylabel("Mean Temperature (°C)")
            plt.grid(True)

            # Ensure only correct days are shown
            plt.xticks(days)  # Explicitly set x-axis ticks only on saved days

            plt.tight_layout()
            plt.show()

        except Exception as e:
            logging.error('Error in plot_lineplot: %s', e)
            raise


# Configure logging
logging.basicConfig(
    filename='weather_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

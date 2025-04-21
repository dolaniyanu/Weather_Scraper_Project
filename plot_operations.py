### PROJECT
### plot_operations.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-20

import matplotlib.pyplot as plt
import matplotlib.pyplot as ticker
from dbcm import DBCM
import sqlite3
from collections import defaultdict
import datetime

class PlotOperations:
    def __init__(self, db_name="weather.sqlite"):
        # Initializes the class with the name of the database being used in PlotOperations class.
        self.db_name = db_name

    def _fetch_data(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sample_date, avg_temp FROM weather")
            return cursor.fetchall()
    
    def prepare_data(self):
        rows = self._fetch_data()
        monthly_data = defaultdict(list)
        daily_data = defaultdict(list)

        for sample_date, avg_temp in rows:
            # Converts the string date into a datetime object
            if avg_temp is not None:
                date_block = datetime.datetime.strptime(sample_date, "%Y-%m-%d")
                month = date_block.month
                year_month = date_block.strftime("%Y-%m")

                # Groups the temperatures by month and by specific year-month combinations.
                monthly_data[month].append(avg_temp)
                daily_data[year_month].append((date_block.day, avg_temp))

        return monthly_data, daily_data
    
    def plot_boxplot(self):
        monthly_data, _ = self.prepare_data()
        plt.figure(figsize=(12, 6))

        # Plot boxplots for each month using the scraped data.
        plt.boxplot([monthly_data[m] for m in range(1, 13)], labels =
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.title("Full Data Monthly Temperature Distribution (Boxplot)")
        plt.xlabel("Month")
        plt.ylabel("Mean Temperature (°C)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_lineplot(self):
        _, daily_data = self.prepare_data()

        # Selects the latest month from the dataset and sorts its data by day
        latest_month = sorted(daily_data.keys())[-1]
        daily_temps = sorted(daily_data[latest_month], key=lambda x: x[0])

        # Separate the data into a days lists and a temperatures lists
        days = [day for day, temp in daily_temps]
        temps = [temp for day, temp in daily_temps]

        plt.figure(figsize=(12, 6))
        plt.plot(days, temps, marker='o')
        plt.title(f"Daily Mean Temperature: {latest_month}")
        plt.xlabel("Day")
        plt.ylabel("Mean Temperature (°C)")
        plt.grid(True)
        
        # Enables x-axis to show integer ticks only.
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        plt.tight_layout()
        plt.show()

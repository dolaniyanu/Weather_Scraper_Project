### PROJECT
### sample_data.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-20
###  GOAL  : " Prints the outputs of the Weather Scraper and it's database 'weather' "

from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

DBOperations.initialize_db()


url_template = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&Year={year}&Month={month}&Day=1&timeframe=2"
scraper = WeatherScraper(url_template)

scraped_data = scraper.scrape()  # Returns a valid dictionary of scraped data.

if scraped_data:
    DBOperations.save_data(scraped_data) # Saves Scraped Data records.
    
    # Display the inserted DB records.
    for row in DBOperations.fetch_data():
        print(row)

else:
    print("No data was scraped.")

plotter = PlotOperations()
plotter.plot_boxplot()
plotter.plot_lineplot()
# Historical News Scraper
This script uses Selenium to scrape historical news articles about a topic over a specified date range.


## Setup
You need Python3 to run this script.
First, install the necessary Python dependcies using:
```
pip install -r requirements.txt
```
You will also need to set up Selenium WebDriver on your computer. You can download it here[https://chromedriver.chromium.org/downloads] for your OS. This script has been tested on Chrome versions 111 and 110.

## Usage
There are four arguments you need to pass to the script:

- `search_term`: The term you want to search for (if there are spaces in your search term, enclose the argument with "")
- `start_date`: The first day you want to obtain historical data for (in the format m/d/y)
- `end_date`: The last day you want to obtain historical data for (in the format m/d/y)
- `output_filename`: The name of the csv file you want to write results to


```
python scraper.py search_term   start_date   end_date   output_filename
```

Sample run:
```
python3 scraper.py "elon musk" 01/01/2023 03/08/2023 musk.csv
```
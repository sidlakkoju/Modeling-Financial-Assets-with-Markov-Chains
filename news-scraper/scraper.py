from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import csv
import tqdm
import argparse
import os


driver = None

def startup(search_term):
    global driver
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    driver.get("https://google.com/")

    # # Load Google news search page
    # driver.get("https://news.google.com/")

    # # Find search box element and input search term
    search_box = driver.find_element(by=By.NAME, value="q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)


    # wait for 5 seconds for the page to load
    time.sleep(1)

    pressed = False
    tabs = driver.find_elements(by=By.CLASS_NAME, value='hdtb-mitem')
    # print(tabs)
    for tab in tabs:
        if tab.text == 'News':
            tab.click()
            time.sleep(2)
            pressed = True
            break
        

    if not pressed:
        tabs = driver.find_elements(by=By.CLASS_NAME, value='O3S9Rb')
        # print(tabs)
        for tab in tabs:
            if tab.text == 'News':
                tab.click()
                time.sleep(2)
                pressed = True
                break


    # # Click "Tools" button to open search tools
    # Wait for the page to load and the Tools button to be clickable
    tools_button = driver.find_element(by=By.ID, value="hdtb-tls")
    # Click the Tools button
    tools_button.click()



def get_results_for_one_day(date):
    global driver
    # wait for two seconds
    time.sleep(0.5)
    # print(date.strftime('%Y-%m-%d'))
    # find the any time button
    any_time_button = driver.find_element(by=By.CLASS_NAME, value="KTBKoe")
    any_time_button.click()


    time.sleep(1)

    try:
        custom_range_button = driver.find_element(by=By.XPATH, value='//*[@id="lb"]/div/g-menu/g-menu-item[8]/div/div/span')
        custom_range_button.click()
    except:
        try:
            custom_range_button = driver.find_element(by=By.XPATH, value='//*[@id="lb"]/div/g-menu/g-menu-item[7]/div/div/span')
            custom_range_button.click()
        except:
            try:
                custom_range_button = driver.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[7]/div/g-menu/g-menu-item[8]/div/div')
                custom_range_button.click()
            except:
                print("Was not able to find custom range button")
            
            



    from_field = driver.find_element(by=By.XPATH, value='//*[@id="OouJcb"]')
    to_field = driver.find_element(by=By.XPATH, value='//*[@id="rzG2be"]')
    go_button = driver.find_element(by=By.XPATH, value='//*[@id="T3kYXe"]/g-button')

    date_string = date.strftime("%m/%d/%Y")
    from_field.clear()
    to_field.clear()
    from_field.send_keys(date_string)
    to_field.send_keys(date_string)

    go_button.click()

    # Find all the search results on the first page
    search_results = driver.find_elements(by=By.CLASS_NAME, value='SoaBEf')
    results = []
    # Loop through each search result and extract the information
    for result in search_results:
        # Extract the name
        name = result.find_element(by=By.CLASS_NAME, value='mCBkyc').text
        # Extract the publisher (if available)
        try:
            publisher = result.find_element(by=By.CLASS_NAME, value='CEMjEf').text
        except:
            publisher = ''
        # Extract the link
        link = result.find_element(by=By.CLASS_NAME, value='WlydOe').get_attribute('href')
        # Extract the description (if available)
        try:
            description = result.find_element(by=By.CLASS_NAME, value='GI74Re').text
        except:
            description = ''
        row = [date_string, name, publisher, link, description]
        results.append(row)
    
    return results



def main():
    global driver


    parser = argparse.ArgumentParser()
    parser.add_argument("search_term", type=str, help="search query")
    parser.add_argument("start_date", type=str, help="first day to save query data, in the format m/d/y")
    parser.add_argument("end_date", type=str, help="final day to save query data, in the format m/d/y")
    parser.add_argument("filename", type=str, help="output csv file")

    # parser.add_argument("-a", "--append", action="store_false", help="append to the given file instead of overwriting it")


    args = parser.parse_args()


    startup(args.search_term)


    start_date = datetime.strptime(args.start_date, '%m/%d/%Y').date()
    end_date = datetime.strptime(args.end_date, '%m/%d/%Y').date()

    # calculate difference between dates
    delta = end_date - start_date

    mode = "w+"
    if os.path.exists(args.filename):
        mode = "a"


    if mode == "w+":         # if file doesn't exist, write header
        with open(args.filename, mode=mode, newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Title", "Publisher", "Link", "Description"])  # header
            for i in tqdm.tqdm(range(delta.days + 1)):
                date = start_date + timedelta(days=i)
                new_results = get_results_for_one_day(date)
                for result in new_results:
                    writer.writerow(result)
    
    else:       # if file exists, append to it
        with open(args.filename, mode=mode, newline='') as file:
            writer = csv.writer(file)
            for i in tqdm.tqdm(range(delta.days + 1)):
                date = start_date + timedelta(days=i)
                new_results = get_results_for_one_day(date)
                for result in new_results:
                    writer.writerow(result)

    # Close the driver
    driver.quit()


if __name__ == '__main__':
    main()
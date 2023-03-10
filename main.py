import time
from dataclasses import dataclass, asdict
import os
import csv
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from random import choice


@dataclass
class Company:
    name: str
    website: str
    linkedin: str

def to_csv(data, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', encoding='utf-16') as f:
        headers = ['name', 'website', 'linkedin']
        writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def webdriversetup(proxy):
    chrome_options = ChromeOptions()
    # chrome_options.add_argument('-profile')
    # chrome_options.add_argument(f'--proxy-server={proxy}')
    # chrome_options.add_argument('-headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.page_load_strategy = "eager"
    # chrome_options.add_argument("-start-maximized")
    driver = Chrome(options=chrome_options)
    return driver

def searchpage(driver, term):
    url = 'https://www.stepstone.de/'
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[data-at="searchbar-keyword-input"]'))).send_keys(term + Keys.RETURN)
    # job page
    endpage = False
    company_urls = list()
    page = 1
    print(f'get data from page {page}')
    # while not endpage:
    while page < 2:
        # accept cookies
        try:
            wait.until(ec.element_to_be_clickable((By.ID, 'ccmgt_explicit_accept'))).click()
        except:
            print('no_cookies')
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-at="unified-resultlist"]')))
        mainwindow = driver.current_window_handle
        parent = driver.find_elements(By.CSS_SELECTOR, 'div[data-resultlist-offers-numbers] > div > article')
        for child in parent:
            try:
                js_code = "arguments[0].scrollIntoView();"
                element = child.find_element(By.CSS_SELECTOR, 'a[data-at="job-item-title"]')
                driver.execute_script(js_code, element)
                element.click()
                time.sleep(5)

                # go to company page
                allwindow = driver.window_handles
                for selwindow in allwindow:
                    # switch focus to child window
                    if (selwindow != mainwindow):
                        driver.switch_to.window(selwindow)
                        # print(driver.page_source)
                        try:
                            company_url = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'a[data-at="header-company-name"]'))).get_attribute('href')
                        except Exception as e:
                            print(e)
                            time.sleep(120)
                            # current_url = driver.current_url
                            # driver.quit()
                            # driver = webdriversetup()
                            # driver.get(current_url)
                            company_url = None
                        company_urls.append(company_url)
                        driver.close()
                        driver.switch_to.window(mainwindow)
            except Exception as e:
                print(e)
                continue

        # Change page
        try:
            page += 1
            print(f'get data from page {page}')
            wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="N??chste"]'))).click()
        except Exception as e:
            print(e)
            endpage = True
            print('complete get all company url')
    input('End Of Script!')
    return company_urls

def main():
    proxies = ['15.204.139.175:8800','15.204.138.215:8800','80.65.220.32:8800','80.65.221.91:8800',
               '15.204.138.188:8800','15.204.139.7:8800','15.204.139.139:8800','15.204.139.10:8800',
               '80.65.220.10:8800','80.65.221.196:8800']
    term = input('Input job position:')
    proxy = choice(proxies)
    print(proxy)
    driver = webdriversetup(proxy=proxy)
    company_urls = searchpage(driver, term)
    print(company_urls)

if __name__ == '__main__':
    main()

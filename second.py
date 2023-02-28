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
    # chrome_options.add_argument('-profile')
    # chrome_options.add_argument(f'--proxy-server={proxy}')
    # chrome_options.add_argument('-headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.page_load_strategy = "eager"
    # chrome_options.add_argument("-start-maximized")
    driver = Chrome(options=chrome_options)
    return driver

def main():
    proxies = ['15.204.139.175:8800', '15.204.138.215:8800', '80.65.220.32:8800', '80.65.221.91:8800',
               '15.204.138.188:8800', '15.204.139.7:8800', '15.204.139.139:8800', '15.204.139.10:8800',
               '80.65.220.10:8800', '80.65.221.196:8800']
    term = input('Input job position:')
    proxy = choice(proxies)
    print(proxy)
    term = term.replace(' ','-').lower()
    url = f'https://www.stepstone.de/jobs/{term}?page=1'
    driver = webdriversetup(proxy=proxy)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    parent = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"] > ul > li')))[-2]
    lastpage = int(parent.text)
    input('Script End')
    driver.quit()
    for page in range(1,lastpage):
        url = f'https://www.stepstone.de/jobs/{term}?page={page}'
        if page % 5 == 0:
            print('Change driver...')
            proxy = choice(proxies)
            print(proxy)
            driver = webdriversetup(proxy=proxy)
            wait = WebDriverWait(driver, 10)
        else:
            proxy = choice(proxies)
            print(proxy)
            driver = webdriversetup(proxy=proxy)
            wait = WebDriverWait(driver, 10)


if __name__ == '__main__':
    main()
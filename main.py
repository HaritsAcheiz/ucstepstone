from dataclasses import dataclass, asdict
import os
import csv
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
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
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument('-headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.page_load_strategy = "eager"
    chrome_options.add_argument("start-maximized")
    driver = Chrome(options=chrome_options)
    return driver

def main():
    proxies = ['192.126.250.22:8800',
               '192.126.253.48:8800',
               '192.126.253.197:8800',
               '192.126.253.134:8800',
               '192.126.253.59:8800',
               '192.126.250.223:8800']
    proxy = choice(proxies)
    driver = webdriversetup(proxy=proxy)
    driver.get('https://www.google.com')
    wait = WebDriverWait(driver, 10)
    title = wait.until(ec.presence_of_element_located((By.TAG_NAME, 'title'))).text
    print(title)

if __name__ == '__main__':
    print(os.getenv('HOME', '/home/haritz/project/venv/ucstepstone'))
    main()

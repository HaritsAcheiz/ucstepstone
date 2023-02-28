import time
from dataclasses import dataclass, asdict
import os
import csv

from selenium.webdriver import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from random import choice
import json
from fake_useragent import UserAgent

@dataclass
class Company:
    name: str
    website: str
    linkedin: str

@dataclass
class StepStoneScraper:
    proxies: list[str]

    def to_csv(self, data, filename, headers):
        file_exists = os.path.isfile(filename)

        with open(filename, 'w', encoding='utf-16') as f:
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)

    def list_to_csv(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def webdriversetup(self, proxy, useragent):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        # chrome_options.add_argument('-headless')
        chrome_options.add_argument(f"--user-agent={useragent}")
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-popup-blocking')
        # chrome_options.add_argument('--window-size=300,700')
        # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--no-first-run')
        # chrome_options.add_argument('--no-service-autorun')
        # chrome_options.add_argument('--password-store=0')
        # chrome_options.add_argument('--incognito')
        chrome_options.page_load_strategy = "eager"
        driver = Chrome(options=chrome_options)
        return driver

    def get_job_urls(self, page_url, job_urls):
        last_proxy = None
        next_proxy = choice(self.proxies)
        ua = UserAgent(browsers=['chrome'])
        while 1:
            if last_proxy == next_proxy:
                next_proxy = choice(self.proxies)
            else:
                break
        print(next_proxy)

        while 1:
            useragent = ua.random
            if 'Linux' in useragent:
                break
            else:
                continue
        print(useragent)

        driver = self.webdriversetup(proxy=next_proxy, useragent=useragent)
        wait = WebDriverWait(driver, 15)
        driver.get(page_url)

        action = ActionChains(driver)
        action.click_and_hold()
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 6)
        action.move_by_offset(1, 8)
        action.release()
        action.perform()
        action.reset_actions()

        parent = wait.until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-resultlist-offers-numbers] > div > article')))
        for child in parent:
            try:
                js_code = "arguments[0].scrollIntoView();"
                element = child.find_element(By.CSS_SELECTOR, 'a[data-at="job-item-title"]')
                driver.execute_script(js_code, element)
                job_url = element.get_attribute('href')
                job_urls.append(job_url)
            except Exception as e:
                print(e)
                continue
        driver.quit()
        return job_urls

    def main(self):
        term = input('Input job position:')
        next_proxy = choice(self.proxies)
        print(next_proxy)
        ua = UserAgent(browsers=['chrome'])
        while 1:
            useragent = ua.random
            if 'Linux' in useragent:
                break
            else:
                continue
        print(useragent)
        term = term.replace(' ','-').lower()
        page_url = f'https://www.stepstone.de/jobs/{term}?page=1'
        driver = self.webdriversetup(proxy=next_proxy, useragent=useragent)
        wait = WebDriverWait(driver, 15)
        driver.get(page_url)

        action = ActionChains(driver)
        action.click_and_hold()
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 1)
        action.move_by_offset(1, 6)
        action.move_by_offset(1, 8)
        action.release()
        action.perform()
        action.reset_actions()

        parent = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-resultlist-offers-numbers] > div > article')))
        file_exists = os.path.isfile('job_urls2.data')
        if not file_exists:
            job_urls = list()
        else:
            with open('job_urls.data2', 'r') as f:
                job_urls = json.load(f)
        for child in parent:
            try:
                js_code = "arguments[0].scrollIntoView();"
                element = child.find_element(By.CSS_SELECTOR, 'a[data-at="job-item-title"]')
                driver.execute_script(js_code, element)
                job_url = element.get_attribute('href')
                job_urls.append(job_url)
            except Exception as e:
                print(e)
                continue
        self.list_to_csv(job_urls, filename='job_urls2.data')
        parent = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"] > ul > li')))[-2]
        lastpage = int(parent.text)
        print(f'Get job url from page 1 of {str(lastpage)}...')
        print(f'{len(job_urls)} job url(s) collected')
        driver.quit()
        for page in range(2,lastpage):
            print(f'Get job url from page {str(page)} of {str(lastpage)}...')
            page_url = f'https://www.stepstone.de/jobs/{term}?page={str(page)}'
            trials = 1
            while trials <= 3:
                try:
                    job_urls = self.get_job_urls(page_url,job_urls=job_urls)
                    self.list_to_csv(job_urls, filename='job_urls2.data')
                    print(f'{len(job_urls)} job url(s) collected')
                    trials = 0
                    break
                except Exception as e:
                    print(e)
                    if trials == 4:
                        print(f'failed to get job url(s) from page {str(page)}')
                        driver.quit()
                    else:
                        trials += 1
                        driver.quit()
        # csv_headers = ['name', 'website', 'linkedin']

if __name__ == '__main__':
    proxies = [
        '80.65.221.12:8800','80.65.220.172:8800','80.65.223.48:8800','80.65.220.133:8800','80.65.221.130:8800',
        '80.65.222.66:8800','80.65.222.138:8800','80.65.223.125:8800','80.65.223.98:8800','80.65.223.188:8800'
    ]
    SSS = StepStoneScraper(proxies=proxies)
    SSS.main()
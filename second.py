import time
from dataclasses import dataclass, asdict
import os
import csv
import re
from selenium.webdriver import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from random import choice, shuffle, uniform
import json
from typing import List
import requests
from selectolax.parser import HTMLParser


@dataclass
class Company:
    name: str
    website: str
    linkedin: str

@dataclass
class StepStoneScraper:
    proxies: List[str]
    useragents: List[str]
    term = str
    last_page = str


    def to_csv(self, data, filename):
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', encoding='utf-16') as f:
            headers = ['name', 'website', 'linkedin']
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def list_to_csv(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def scrambled(self, orig):
        dest = orig[:]
        shuffle(dest)
        return dest

    def webdriversetup(self, proxy, useragent):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        chrome_options.add_argument('-headless')
        chrome_options.add_argument(f"--user-agent={useragent}")
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-popup-blocking')
        # chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--no-first-run')
        # chrome_options.add_argument('--no-service-autorun')
        # chrome_options.add_argument('--password-store=0')
        # chrome_options.add_argument('--incognito')
        chrome_options.page_load_strategy = "eager"
        driver = Chrome(options=chrome_options)
        return driver

    def get_company_name(self, page_url, company_names):
        last_proxy = None
        next_proxy = choice(self.proxies)
        # ua = UserAgent(browsers=['chrome'])
        while 1:
            if last_proxy == next_proxy:
                next_proxy = choice(self.proxies)
            else:
                break
        print(next_proxy)

        # while 1:
        #     useragent = ua.random
        #     if 'Linux' in useragent:
        #         break
        #     else:
        #         continue
        # print(useragent)

        useragent=choice(self.useragents)
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
                # job_link = child.find_element(By.CSS_SELECTOR, 'a[data-at="job-item-title"]')
                cmp_name = child.find_element(By.CSS_SELECTOR, 'span[data-at="job-item-company-name"]')
                driver.execute_script(js_code, cmp_name)
                # job_url = job_link.get_attribute('href')
                company_name = cmp_name.text
                if company_name in company_names:
                    pass
                else:
                    company_names.append(company_name)
            except Exception as e:
                print(e)
                continue
            time.sleep(uniform(0.1, 1.0))
        driver.quit()
        return company_names

    def initiate(self):
        next_proxy = choice(self.proxies)
        print(next_proxy)
        # ua = UserAgent(browsers=['chrome'])
        # while 1:
        #     useragent = ua.random
        #     if 'Linux' in useragent:
        #         break
        #     else:
        #         continue
        # print(useragent)
        useragent = choice(self.useragents)
        print(useragent)
        term = self.term.replace(' ', '-').lower()
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

        parent = wait.until(ec.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-resultlist-offers-numbers] > div > article')))
        file_exists = os.path.isfile(f'{self.term}.data')
        if not file_exists:
            company_names = list()
        else:
            with open(f'{self.term}.data', 'r') as f:
                company_names = json.load(f)
        for child in parent:
            try:
                js_code = "arguments[0].scrollIntoView();"
                # job_link = child.find_element(By.CSS_SELECTOR, 'a[data-at="job-item-title"]')
                cmp_name = child.find_element(By.CSS_SELECTOR, 'span[data-at="job-item-company-name"]')
                driver.execute_script(js_code, cmp_name)
                # job_url = job_link.get_attribute('href')
                company_name = cmp_name.text
                if company_name in company_names:
                    pass
                else:
                    company_names.append(company_name)
            except Exception as e:
                print(e)
                continue
            time.sleep(uniform(0.1, 1.0))
        self.list_to_csv(company_names, filename=f'{self.term}.data')
        parent = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"] > ul > li')))[-2]
        self.lastpage = int(parent.text)
        print(f'Get company name from page 1 of {str(self.lastpage)}...')
        print(f'{len(company_names)} company name(s) collected')
        driver.quit()
        return company_names

    def paginationbelowlimit(self, company_names):
        # for page in range(2,30):
        for page in range(2, self.lastpage):
            print(f'Get company name from page {str(page)} of {str(self.lastpage)}...')
            page_url = f'https://www.stepstone.de/jobs/{self.term}?page={str(page)}'
            trials = 1
            while trials <= 3:
                try:
                    company_names = self.get_company_name(page_url, company_names=company_names)
                    self.list_to_csv(company_names, filename=f'{self.term}.data')
                    print(f'{len(company_names)} company name (s) collected')
                    trials = 0
                    break
                except Exception as e:
                    print(e)
                    if trials == 3:
                        print(f'failed to get company name(s) from page {str(page)}')
                        # driver.quit()
                    else:
                        trials += 1
                        # driver.quit()

    def paginationoverlimit(self, company_names):
        for page in range(2,30):
            print(f'Get company name from page {str(page)} of {str(self.lastpage)}...')
            page_url = f'https://www.stepstone.de/jobs/{self.term}?page={str(page)}'
            trials = 1
            while trials <= 3:
                try:
                    company_names = self.get_company_name(page_url, company_names=company_names)
                    self.list_to_csv(company_names, filename=f'{self.term}.data')
                    print(f'{len(company_names)} company name (s) collected')
                    trials = 0
                    break
                except Exception as e:
                    print(e)
                    if trials == 3:
                        print(f'failed to get company name(s) from page {str(page)}')
                        # driver.quit()
                    else:
                        trials += 1

    def read_company_name(self):
        with open(f'{self.term}.data', 'r') as f:
            company_list = json.load(f)
        return company_list

    def get_company_url(self, company_list):
        print("Searching for company url...")
        last_proxy = None
        current_proxy = None
        while last_proxy == current_proxy:
            current_proxy = choice(self.proxies)

        formated_proxies = {
            "http": f"http://{current_proxy}",
            "https": f"http://{current_proxy}"
        }

        header = {
            "user-agent": choice(self.useragents)
        }
        count = 0
        for company_name in company_list:
            print(f"Searching for {company_name} url...")
            linkedin_url = f"https://html.duckduckgo.com/html/?q={re.sub('[^A-Za-z0-9]+', '+', company_name)}+linkedin"
            web_url = f"https://html.duckduckgo.com/html/?q={re.sub('[^A-Za-z0-9]+', '+', company_name)}"
            with requests.Session() as client:
                response = client.get(web_url, headers=header, proxies=formated_proxies, timeout=(5, 27))
            print(response)
            print(response.text)
            tree = HTMLParser(response.text)
            company_website = tree.css_first("div.serp__results > div#links.results > div.result.results_links.results_links_deep.web-result > div.links_main.links_deep.result__body > div.result__extras > div.result__extras__url > a.result__url").text().strip()
            with requests.Session() as client:
                response = client.get(linkedin_url, headers=header, proxies=formated_proxies, timeout=(5, 27))
            print(response)
            print(response.text)
            tree = HTMLParser(response.text)
            company_linkedin = tree.css_first("div.serp__results > div#links.results > div.result.results_links.results_links_deep.web-result > div.links_main.links_deep.result__body > div.result__extras > div.result__extras__url > a.result__url").text().strip()

            new_item = asdict(Company(name=company_name, website=company_website, linkedin=company_linkedin))
            self.to_csv(new_item, f'{self.term}.csv')
            print(f"{company_name} url collected")
            count += 1
        print(f"{count} company data(s) collected")

    def main(self):
        self.term = input('Input job position:')
        company_names = self.initiate()
        if self.lastpage > 30:
            self.paginationoverlimit(company_names)
        else:
            self.paginationbelowlimit(company_names)
        company_lists = self.read_company_name()
        self.get_company_url(company_lists)

if __name__ == '__main__':
    proxies = [
        '80.65.221.12:8800', '80.65.220.172:8800', '80.65.223.48:8800', '80.65.220.133:8800', '80.65.221.130:8800',
        '80.65.222.66:8800', '80.65.222.138:8800', '80.65.223.125:8800', '80.65.223.98:8800', '80.65.223.188:8800'
    ]

    useragents =[
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5503.200 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/110.0.5481.100 Safari/537.36',
        'Mozilla/5.0 (Linux x86_64; en-US) AppleWebKit/537.45 (KHTML, like Gecko) Chrome/113.0.5503.200 Safari/534',
        'Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/602.18 (KHTML, like Gecko) HeadlessChrome/110.0.5481.100 Safari/600'
    ]

    SSS = StepStoneScraper(proxies=proxies, useragents=useragents)
    SSS.main()
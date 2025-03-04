#scraper.py
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import logging
from urllib.parse import urljoin

class WebScraper:
    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url):
        try:
            sleep(self.delay)  # Respect the site by waiting between requests
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def extract_data(self, soup, selectors):
        data = {}
        for name, selector in selectors.items():
            try:
                element = soup.select_one(selector)
                data[name] = element.text.strip() if element else ''
            except Exception as e:
                self.logger.error(f"Error extracting {name}: {str(e)}")
                data[name] = ''
        return data

    def save_to_csv(self, data, filename):
        if not data:
            self.logger.warning("No data to save")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            self.logger.info(f"Data saved to {filename}")
        except IOError as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")

    def scrape_pages(self, urls, selectors):
        all_data = []
        for url in urls:
            full_url = urljoin(self.base_url, url)
            self.logger.info(f"Scraping {full_url}")
            
            soup = self.fetch_page(full_url)
            if soup:
                data = self.extract_data(soup, selectors)
                data['url'] = full_url
                all_data.append(data)
                
        return all_data

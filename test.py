from scraper import WebScraper
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Example usage
scraper = WebScraper('https://quotes.toscrape.com', delay=2)

# Define what data to extract
selectors = {
    'title': 'h1',
    'description': '.description',
    'paragraphs' : 'p',
    'spans' : 'span'
}

# URLs to scrape
urls = [
    '/',
]

# Scrape the pages
data = scraper.scrape_pages(urls, selectors)

input = f"""summarize what the website does in under 50 words using the following data:
 {data}"""

response = model.generate_content(input)
print(response.text)

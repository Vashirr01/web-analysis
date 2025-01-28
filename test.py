# from scraper import WebScraper
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)

# # Example usage
# scraper = WebScraper('https://www.mathacademy.com', delay=2)
#
# # Define what data to extract
# selectors = {
#     'title': 'h1',
#     'description': '.description',
#     'paragraphs' : 'p'
# }
#
# # URLs to scrape
# urls = [
#     '/',
# ]
#
# # Scrape the pages
# data = scraper.scrape_pages(urls, selectors)
#
# # Save results
# scraper.save_to_csv(data, 'scraped_data.csv')

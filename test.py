import sys
import json
from scraper import WebScraper
import google.generativeai as genai
from dotenv import load_dotenv
import os

def main(url):
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Initialize scraper
    scraper = WebScraper(url, delay=2)
    
    # Define selectors
    selectors = {
        'title': 'h1',
        'description': '.description',
        'paragraphs': 'p',
        'spans': 'span'
    }
    
    # Scrape the page
    scraped_data = scraper.scrape_pages(['/'], selectors)
    
    # Generate summary
    prompt = f"Summarize what the website does in under 100 words using the following data:\n{scraped_data}"
    response = model.generate_content(prompt)
    
    # Prepare result
    result = {
        'scraped_data': scraped_data,
        'summary': response.text
    }
    
    # Print as JSON for Go to parse
    print(json.dumps(result))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scraper_script.py <url>")
        sys.exit(1)
    main(sys.argv[1])

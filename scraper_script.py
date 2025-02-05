# scraper_script.py
import sys
import json
from scraper import WebScraper
import google.generativeai as genai
from dotenv import load_dotenv
import os

def main(url):
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("GEMINI_API")
        if not api_key:
            raise ValueError("GEMINI_API key not found in environment")
            
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
        
        # Prepare and print result as JSON
        result = {
            'scraped_data': scraped_data,
            'summary': response.text
        }
        
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        # Print error as JSON
        error_result = {
            'error': str(e),
            'scraped_data': None,
            'summary': None
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'URL argument required'}), file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])

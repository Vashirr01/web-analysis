from scraper import WebScraper

# Example usage
scraper = WebScraper('https://csprimer.com', delay=2)

# Define what data to extract
selectors = {
    'title': 'h1',
    'description': '.description'
}

# URLs to scrape
urls = [
    '/',
    '/courses/'
]

# Scrape the pages
data = scraper.scrape_pages(urls, selectors)

# Save results
scraper.save_to_csv(data, 'scraped_data.csv')

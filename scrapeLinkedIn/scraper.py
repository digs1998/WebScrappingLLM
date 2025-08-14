
from crawlee.playwright_crawler import PlaywrightCrawler
from .gptDomainExtractor import addDomainInsights
from .routes import router
import pandas as pd
import urllib.parse 
import asyncio                                

async def scrapeLinkedIn(title: str, location: str, data_name: str) -> None:
    base_url = "https://www.linkedin.com/jobs/search"

    # URL encode the parameters
    params = {
        "keywords": title,
        "location": location,
        "trk": "public_jobs_jobs-search-bar_search-submit",
        "position": "1",
        "pageNum": "0"
    }
    encoded_params = urllib.parse.urlencode(params)
    encoded_url = f"{base_url}?{encoded_params}"

    # Initialize the crawler
    crawler = PlaywrightCrawler(
        request_handler=router,
        headless=False,
        max_requests_per_crawl=50,
        browser_type='webkit'
    )

    # Run the crawler with the initial list of URLs
    await crawler.run([
        encoded_url
        
        ])

    # Save the data in a CSV file
    output_file = f"{data_name}.csv"
    await crawler.export_data(output_file)
    
    df = pd.read_csv(output_file)
    df = addDomainInsights(df)
    
    df['title'] = df['title'].str.replace(r'(?<!^)(?=[A-Z])', ' ', regex=True)
    df['Time of posting'] = df['Time of posting'].str.replace(r'(?<!^)(?=[A-Z])', ' ', regex=True)
    df = df.drop('url', axis=1)
    return df
    
# if __name__ == "__main__":
#     title = "Data Scientist"
#     location_name = "United States"
#     data_name = "jobApplications"
#     asyncio.run(main(title, location_name, data_name))
import asyncio
import random
import re
from crawlee.router import Router
from crawlee import Request
from crawlee.playwright_crawler import PlaywrightCrawlingContext

# List of rotating User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
]

router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    """Default request handler."""
    # Random delay between requests to avoid 429s
    await asyncio.sleep(random.uniform(3, 7))

    # Rotate user agent
    await context.page.set_extra_http_headers({
        "User-Agent": random.choice(USER_AGENTS)
    })

    # Select all job posting links
    hrefs = await context.page.locator(
        'ul.jobs-search__results-list a'
    ).evaluate_all("links => links.map(link => link.href)")

    # Add job links to queue
    await context.add_requests([
        Request.from_url(rec, label='job_listing') for rec in hrefs
    ])

@router.handler('job_listing')
async def listing_handler(context: PlaywrightCrawlingContext) -> None:
    """Handler for job listings."""
    await asyncio.sleep(random.uniform(3, 6))  # delay between detail page fetches

    # Rotate user agent
    await context.page.set_extra_http_headers({
        "User-Agent": random.choice(USER_AGENTS)
    })

    await context.page.wait_for_load_state('load')

    job_title = await context.page.locator(
        '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1'
    ).text_content()

    company_name = await context.page.locator(
        '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a'
    ).text_content()

    time_of_posting = await context.page.locator(
        '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span'
    ).text_content()

    await context.push_data({
        'title': re.sub(r'[\s\n]+', '', job_title or ""),
        'Company name': re.sub(r'[\s\n]+', '', company_name or ""),
        'Time of posting': re.sub(r'[\s\n]+', '', time_of_posting or ""),
        'url': context.request.loaded_url,
    })

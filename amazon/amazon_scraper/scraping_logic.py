# amazon_scraper/scraping_logic.py
import httpx
import json
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from amazon_scraper.models import Product  # Import your Product model here

@dataclass
class Store:
    name: str
    url: str
    title: str
    price: str
    description: str

@dataclass
class Item:
    store: Store
    title: str
    price: str
    description: str

def load_stores():
    with open("stores.json", 'r') as f:
        data = json.load(f)

    return [Store(**item) for item in data]

async def load_page(client, url, method="GET"):  # Allow specifying request method
    async with client.stream(method, url) as resp:
        if resp.status_code == 200:
            return HTMLParser(await resp.aread())

def parse(store, html):
    return Item(store=store,
                title=html.css_first(store.title).text(strip=True),
                price=html.css_first(store.price).text(strip=True),
                description=html.css_first(store.description).text(strip=True)
                )

def store_selector(stores, url):
    for store in stores:
        if store.url in url:
            return store

async def scrape_amazon_data(url):
    try:
        stores = load_stores()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }

        async with httpx.AsyncClient(headers=headers) as client:
            store = store_selector(stores, url)
            html = await load_page(client, url, method="POST")  # Use POST method
            item = parse(store, html)

            # Save the scraped data to the database
            product = Product(title=item.title, price=item.price, description=item.description, url=url)
            product.save()

            return product

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def main():
    urls = [
        "https://rab.equipment/uk/electron-pro-jacket",
        "https://www.fjallraven.com/uk/en-gb/men/jackets/shell-jackets/keb-eco-shell-jacket-m",
    ]

    for url in urls:
        product = await scrape_amazon_data(url)
        if product:
            print(f"Scraped: {product.title}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import asyncio
import aiohttp
import time
import requests
from concurrent.futures import ThreadPoolExecutor


URLS = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://www.python.org",
    "https://www.google.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.wikipedia.org",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.reddit.com",
]

# Async version with aiohttp
def print_title(title):
    print(f"Fetched: {title}")

async def fetch(session, url):
    """Fetch a URL and print its title.
     Args:
         session: aiohttp ClientSession
         url: URL to fetch
     Returns:
         The response text
    """
    async with session.get(url) as resp:
        text = await resp.text()
        print_title(url)
        return text

async def async_crawler():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in URLS]
        return await asyncio.gather(*tasks)

# Multi-thread version with requests
def fetch_sync(url):
    resp = requests.get(url)
    print_title(url)
    return resp.text

def threaded_crawler():
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(fetch_sync, URLS))

if __name__ == "__main__":
    print("--- Asyncio version ---")
    start = time.time()
    asyncio.run(async_crawler())
    print(f"Asyncio done in {time.time() - start:.2f}s\n")

    print("--- Threaded version ---")
    start = time.time()
    threaded_crawler()
    print(f"Threaded done in {time.time() - start:.2f}s\n")

    # Hands-on: thử tạo event loop, chạy nhiều task nhỏ, in ra kết quả
    # Gợi ý: asyncio.create_task, asyncio.sleep, asyncio.get_event_loop

"""
Asynchronous Web Scraper

This script uses asynchronous programming with aiohttp and asyncio to download images from a website.

Dependencies:
- aiofiles: Asynchronous file operations.
- aiohttp: Asynchronous HTTP client.
- asyncio: Asynchronous programming library.
- selectolax.parser: HTML parser for selecting elements in an HTML document.
- os: Operating system-related functionality.

Author: [Your Name]
Date: [Current Date]

"""

import aiofiles
import aiohttp
import asyncio
from selectolax.parser import HTMLParser
import os

# Global list to store downloaded image names
data = []

async def write_file(session, url, name_f):
    """
    Asynchronously downloads and saves an image from a given URL.

    Parameters:
    - session (aiohttp.ClientSession): Asynchronous HTTP client session.
    - url (str): URL of the image.
    - name_f (str): Name for the saved image file.

    Returns:
    None
    """
    async with aiofiles.open(f'all_images/{name_f}.jpg', mode='wb') as file, \
            session.get(url) as response:
        async for x in response.content.iter_chunked(2048):
            await file.write(x)
        print('Image_Save!', name_f + '.jpg')

async def content_download(session, url):
    """
    Asynchronously downloads content from a given URL and extracts image URLs for download.

    Parameters:
    - session (aiohttp.ClientSession): Asynchronous HTTP client session.
    - url (str): URL to download content from.

    Returns:
    None
    """
    async with session.get(url) as response:
        htm_obj = HTMLParser(await response.text())
        link_urls = [link.attrs.get('src') for link in htm_obj.css('.picture')]
        tasks = [asyncio.create_task(write_file(session, link, name))
         for link in link_urls if (name := ''.join(link.split('/')[-1])[:-4]) not in data]

        await asyncio.gather(*tasks)

async def main():
    """
    Asynchronous main function to initiate the web scraping process.

    Returns:
    None
    """
    main_url = 'https://parsinger.ru/asyncio/aiofile/2/index.html'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=main_url) as response:
            html_obj = HTMLParser(await response.text())
            link_urls = [
                f'https://parsinger.ru/asyncio/aiofile/2/{link.attrs.get("href")}' for link in html_obj.css('.item_card > a')]

            tasks = [content_download(session, link) for link in link_urls]
            await asyncio.gather(*tasks)

print(asyncio.run(main()))

# Calculate and print the total size of the downloaded images folder
size = 0
Folderpath = '/home/murs/async_parser/all_images'

for path, dirs, files in os.walk(Folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)

print("Folder size: " + str(size))

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# Chrome options setup
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_experimental_option("detach", True)

# Instantiate the Chrome driver with the configured options
driver = webdriver.Chrome(options=chrome_options)

# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to download an image
def download_image(image_url, folder_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = os.path.basename(urlparse(image_url).path)
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {image_name}")
    else:
        print(f"Failed to download: {image_url}")

# Function to crawl a webpage and return unique same-site URLs
def crawl_webpage(base_url, site_domain, crawled_urls):
    driver.get(base_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
	
    # Get the website's domain name to use as the folder name
    domain_name = urlparse(base_url).netloc
    folder_name = domain_name.replace('.', '_')
    create_folder(folder_name)

    # Find and download images
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_url = urljoin(base_url, img_tag.get('src'))
        download_image(img_url, folder_name)

    print(f"Crawled: {base_url}")

    # Find and return unique same-site URLs
    new_urls = set()
    anchor_tags = soup.find_all('a', href=True)
    for anchor_tag in anchor_tags:
        new_url = urljoin(base_url, anchor_tag['href'])
        new_url_domain = urlparse(new_url).netloc
        if new_url_domain == site_domain and new_url not in crawled_urls:
            new_urls.add(new_url)
            print('New Url Found: '+new_url)
		
    return new_urls

# Starting URL
starting_url = 'https://www.ant1live.com/'  # Replace with your starting URL

# Get the domain name of the starting URL
site_domain = urlparse(starting_url).netloc

# List to keep track of crawled URLs
crawled_urls = set()

# Add the starting URL to the list
crawled_urls.add(starting_url)

# Crawl and populate URLs dynamically
urls_to_crawl = {starting_url}

while urls_to_crawl:
    url = urls_to_crawl.pop()
    new_urls = crawl_webpage(url, site_domain, crawled_urls)
    crawled_urls.update(new_urls)
    urls_to_crawl.update(new_urls)

print("Crawling completed.")

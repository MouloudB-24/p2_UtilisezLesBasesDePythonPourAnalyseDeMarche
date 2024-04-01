import sys

import requests
from bs4 import BeautifulSoup

from a_single_book_category import get_category_data


def get_all_data(base_url):
    """
    Scrapes data for all book categories from the base url.

    :param base_url: Books to Scrape website url.
    :return: None.
    """
    n = 1
    urls_category = get_category_urls(base_url)
    for url_of_category in urls_category:
        print(f'Scraping category {n}/{len(urls_category)} ...')
        get_category_data(url_of_category)
        n += 1


# Function for retrieves all URLs of book categories
def get_category_urls(base_url):
    """
    Retrieves all URLs for all book categories.

    :param base_url: The starting URL for book categories.
    :return: List of all book category URLs.
    """

    response = requests.get(base_url)
    response.encoding = response.apparent_encoding

    # Check response status
    if response.status_code != 200:
        print(f"HTTP request error status code: {response.status_code}")
        sys.exit()

    # Use BeautifulSoup to analyze the page's HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract book category URLs
    category_a = soup.find('ul', class_='nav nav-list').find_all('a')
    urls_of_categories = [base_url + url.get('href') for url in category_a[1:]]

    return urls_of_categories


# Example of use
if __name__ == '__main__':
    get_category_urls("https://books.toscrape.com/")

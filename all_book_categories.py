import requests
from bs4 import BeautifulSoup

from a_single_book_category import get_category_data
from my_library import BASE_URL


def get_all_data(url):
    """
    Scrapes data for all book categories from the base url.

    :param url: BASE_URL
    :return: None
    """
    n = 1
    for url in get_category_urls(url):
        print(f'Scraping category {n}/{len(get_category_urls(url))} ...')
        get_category_data(url)
        n += 1


# Function for retrieves all URLs of book categories
def get_category_urls(url):
    """
    Retrieves all URLs for all book categories.

    :param url: The starting URL for book categories.
    :return: List of all book category URLs.
    """

    response = requests.get(url)
    response.encoding = response.apparent_encoding

    # Check response status
    if response.status_code != 200:
        return f"HTTP request error status code: {response.status_code}"

    # Use BeautifulSoup to analyze the page's HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract book category URLs
    category_a = soup.find('ul', class_='nav nav-list').find_all('a')
    urls_of_categories = [BASE_URL + url.get('href') for url in category_a[1:]]

    return urls_of_categories


if __name__ == '__main__':
    get_all_data(BASE_URL)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

from a_single_book import get_book_data
from my_library import BASE_URL, clean_text


def get_category_data(url):
    for url in tqdm(get_all_urls_in_a_category(url)):
        get_book_data(url)


def get_all_urls_in_a_category(url):
    """
    Scrapes all URLs for books a given category.

    :param url: the starting URL if the category
    :return: List of all URLs for books in a given category
    """
    urls_of_books = []

    # Create a session to manage HTTP requests
    with requests.Session() as session:
        while True:
            response = session.get(url)

            # Check response status
            if response.status_code != 200:
                return f"HTTP request error status code: {response.status_code}"

            # Use BeautifulSoup to analyze the page's HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Get URLs on the current page
            books_urls = extract_book_urls_on_page(soup)

            # Add urls of book on the current pages to the "urls_of_books" list
            urls_of_books.extend(books_urls)

            # Get the URL for the next page
            url = get_next_page_url(url, soup)

            # Check if there is no next page
            if not url:
                break

    return urls_of_books


def extract_book_urls_on_page(soup):
    """
    Extracts book URLs from a page.

    :param soup: BeautifulSoup object representing the HTML page
    :return: List of book URLs on the page
    """
    try:
        books_urls_nodes = soup.find_all("h3")
        # Use a list comprehension for constructing URLs
        urls_of_books_a = [url.find('a')["href"] for url in books_urls_nodes]
        return [BASE_URL + "catalogue/" + clean_text(url) for url in urls_of_books_a]

    except Exception as e:
        print(f"Error when extracting book urls : {e}")
        return []


def get_next_page_url(url, soup):
    """
    Gets the URL of the next page.
    :param url: Current page URL
    :param soup: BeautifulSoup object representing the HTML page
    :return: URL of the next page OR False if there is on next page
    """
    next_page_element = soup.find('li', class_="next")

    # Check if there is a next page
    if not next_page_element:
        return False

    # Extract the URL of the next page
    next_page_url = next_page_element.find('a', href=True)

    # Construct the URL for the next page
    if next_page_url:
        return urljoin(url, next_page_url["href"])
    return False


# Example of use
if __name__ == '__main__':
    get_category_data("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")


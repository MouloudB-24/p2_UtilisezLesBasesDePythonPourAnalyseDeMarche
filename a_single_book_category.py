import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


from a_single_book import get_book_data
from my_library import BASE_URL, clean_text


def get_category_data(url_of_category):
    """
    Get all data for a book category

    :param url_of_category: the starting URL if the category.
    :return: None.
    """
    for url_of_book in tqdm(get_all_urls_in_a_category(url_of_category)):
        try:
            get_book_data(url_of_book)

        except Exception as e:
            print(f"Error on this URL {url_of_book}: {e}")


def get_all_urls_in_a_category(url_of_category):
    """
    Scrapes all URLs for books a given category.

    :param url_of_category: the starting URL if the category
    :return: List of all URLs for books in a given category
    """
    urls_of_books_on_all_pages = []

    # Create a session to manage HTTP requests
    with requests.Session() as session:
        while True:
            # Make a GET request to the book URL
            response = session.get(url_of_category)

            # Check response status
            if response.status_code != 200:
                print(f"HTTP request error status code: {response.status_code}")
                sys.exit()

            # Use BeautifulSoup to analyze the page's HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Get URLs on the current page
            urls_of_books_on_page = extract_book_urls_on_page(soup)

            # Add urls of book on the current pages to the "urls_of_books_on_all_pages" list
            urls_of_books_on_all_pages.extend(urls_of_books_on_page)

            # Get the URL for the next page
            url_of_category = get_next_page_url(url_of_category, soup)

            # Check if there is no next page
            if not url_of_category:
                break

    return urls_of_books_on_all_pages


def extract_book_urls_on_page(soup):
    """
    Extracts book URLs from a page.

    :param soup: BeautifulSoup object representing the HTML page
    :return: List of book URLs on the page
    """
    try:
        books_urls_nodes = soup.find_all("h3")
        # Use a list comprehension for constructing URLs
        urls_of_books_a = [url_of_book.find('a')["href"] for url_of_book in books_urls_nodes]
        return [BASE_URL + "catalogue/" + clean_text(url_of_book) for url_of_book in urls_of_books_a]

    except Exception as e:
        print(f"Error when extracting book urls : {e}")
        return []


def get_next_page_url(current_page_url, soup):
    """
    Gets the URL of the next page.

    :param current_page_url: Current page URL.
    :param soup: BeautifulSoup object representing the HTML page.
    :return: URL of the next page OR False if there is no next page.
    """
    next_page_element = soup.find('li', class_="next")

    # Check if there is a next page
    if not next_page_element:
        return False

    # Extract the URL of the next page
    next_page_url = next_page_element.find('a', href=True)

    # Construct the URL for the next page
    if next_page_url:
        return urljoin(current_page_url, next_page_url["href"])
    return False


# Example of use
if __name__ == '__main__':
    get_category_data("https://books.toscrape.com/catalogu/category/books/travel/index.html")
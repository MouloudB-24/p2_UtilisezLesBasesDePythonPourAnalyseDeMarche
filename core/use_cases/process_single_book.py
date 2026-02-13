import sys
from bs4 import BeautifulSoup
import requests

from core.extract.book_parser import extract_book_data
from core.load.book_loader import save_book_data, save_book_images
from core.transform.book_transformer import transform_book_data


# Function to extract data from a book
def get_book_data(url_of_book):
    """
    Retrieves data for a single book.

    :param url_of_book: The URL of the book.
    :return: Data for a given book.
    """
    # Create a session to manage HTTP requests
    with requests.Session() as session:
        # Make a GET request to the book URL
        response = session.get(url_of_book)

        # Check response status
        if response.status_code != 200:
            print(f"HTTP request error status code: {response.status_code}")
            sys.exit()

        # Use BeautifulSoup to analyze the page's HTML
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract raw data from a book
        raw_book_data = extract_book_data(url_of_book, soup)

        # Transform book data
        clean_book_data = transform_book_data(raw_book_data)

        # Load data from a book / Save data in a CSV file and book image
        download_folder = save_book_data(clean_book_data, clean_book_data['category'])
        save_book_images(clean_book_data["image_url"], clean_book_data["title"], download_folder, session)

        return clean_book_data
    

# Example of use
if __name__ == '__main__':
    get_book_data("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")
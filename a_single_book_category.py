import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from my_library import BASE_URL,  clean_text


# Scrape all urls for all books in a category
def scrap_book_urls(url):
    # Create a session to manage HTTP requests
    with requests.session() as session:
        urls_of_books = []

        while True:
            response = session.get(url)

            # Check response status
            if response.status_code != 200:
                return f"HTTP request error status code: {response.status_code}"

            # Use BeautifulSoup to analyze the page's HTML
            soup = BeautifulSoup(clean_text(response.text), "html.parser")

            # Pagination
            title_h3 = soup.find_all("h3")
            link_a = [link.find('a')["href"] for link in title_h3]

            # Use a list comprehension for constructing URLs
            urls_of_books.extend([BASE_URL + "catalogue/" + link for link in link_a])

            next_page_element = soup.find('li', class_="next")

            # Exit the program if there is no next page
            if not next_page_element:
                break

            next_page = next_page_element.find('a')
            next_page_url = next_page.get('href')

            # Construct the URL for the next page
            url = urljoin(url, next_page_url)

    return urls_of_books

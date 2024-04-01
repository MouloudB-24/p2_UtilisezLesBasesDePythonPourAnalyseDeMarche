import csv
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from my_library import BASE_URL, clean_text, clean_title


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


# Function for scrapping raw book data
def extract_book_data(url_of_book, soup, category="", title=""):
    """
    Extracts information from a book.

    :param url_of_book: The URL of the book.
    :param soup: BeautifulSoup object representing the page's HTML.
    :param category: The category of the book.
    :param title: The title of the book.
    :return: The dictionary containing raw book data.
    """
    # Extract information from the book
    if not title:
        title = soup.find('h1').text if soup.find('h1') else "Title not found on the page"

    # Category
    if not category:
        category_a = soup.find('ul', class_="breadcrumb").find_all('a')
        category = category_a[2].text if len(category_a) >= 2 else "Category not found on the page"

    # Table information
    if soup.find('table'):
        table_td = soup.find('table').find_all('td')
        table = [information.text for information in table_td]
        # UPC
        universal_product_code = table[0]
        # Price
        price_excluding_tax = table[2]
        price_including_tax = table[3]
        # Number available
        number_available = table[5].split('(')[-1].split(' ')[0]
    else:
        universal_product_code = "UPC not found on the page"
        price_excluding_tax = "Price_ex not found on the page"
        price_including_tax = "Price_in not found on the page"
        number_available = "number_available not found on the page"

    # image_url
    if soup.find('div', class_='item active'):
        image_url_div = soup.find('div', class_='item active').find('img')
        image_url = BASE_URL + image_url_div['src']
    else:
        image_url = "image_url not found on the page"

    # Review rating
    p_star = soup.find('p', class_='star-rating')
    review_rating = p_star['class'][1] if p_star else "Review rating not found on the page"

    # Description
    description_ar = soup.find('article', class_='product_page')
    description_p = description_ar.find('p', recursive=False)
    description = description_p.text if description_p else 'Description not found on the page'

    # Summary of book scraper information
    raw_book_data = {"title": title,
                     "category": category,
                     "universal_product_code": universal_product_code,
                     "product_page_url": url_of_book,
                     'image_url': image_url,
                     "price_excluding_tax": price_excluding_tax,
                     'price_including_tax': price_including_tax,
                     "number_available": number_available,
                     "review_rating": review_rating,
                     "product_description": description}
    return raw_book_data


# Function for cleaning data
def transform_book_data(raw_data):
    """
    Transforms raw book data into clean data.

    :param raw_data: Raw book data as a dictionary.
    :return: Transformed book data as a dictionary.
    """
    clean_book_data = {}
    for keys, value in raw_data.items():
        if keys == "title":
            value = clean_title(value)
        value = clean_text(value)
        clean_book_data[keys] = value
    return clean_book_data


# Function to save scraper data in a CSV file
def save_book_data(clean_data, category, current_folder=Path.cwd()):
    """
    Save book data in a CSV file.

    :param clean_data: Clean book data as a dictionary.
    :param category: The category of the book.
    :param current_folder: The folder where the file CSV will be saved.
    :return: The folder where book images are saved."""

    # Create save folders
    download_folder = current_folder / 'all_book_categories' / category / 'images_of_books'
    download_folder.mkdir(exist_ok=True, parents=True)

    # Create CSV file path
    save_csv_file = download_folder.parent / (category + '.csv')

    # Open CSV file in add mode
    with open(save_csv_file, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # # Check if the file is empty, write the headers
        if file.tell() == 0:
            writer.writerow(clean_data.keys())

        # Write book data to CSV file
        writer.writerow(clean_data.values())

    return download_folder


# Function for downloading and saving book images
def save_book_images(url_of_book_img, title, download_folder, session):
    """
    Saves book images in a specified folder.

    :param url_of_book_img: URL of the book image.
    :param title: The title of the book.
    :param download_folder: The folder where the book images will be saved.
    :return: None
    """

    # Make a GET request to obtain the image
    response = session.get(url_of_book_img)

    save_jpg_file = download_folder / Path(title + '.jpg')

    # Check if the image exists in the folder
    if save_jpg_file.exists():
        return

    # Save image in folder
    with open(save_jpg_file, 'wb') as file:
        file.write(response.content)


# close the HTTP request session
# session.close()

# Example of use
if __name__ == '__main__':
    get_book_data("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")

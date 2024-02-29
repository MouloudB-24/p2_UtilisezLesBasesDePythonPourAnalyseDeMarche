import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from my_library import BASE_URL, clean_text, clean_title

# Initialization of global variables
category = ""
title = ""
download_folder = ""


# Create a session to manage HTTP requests
session = requests.session()


# Function to extract data from a book
def scrap_book_data(url):
    global category, title

    # Make a GET request to the book URL
    response = session.get(url)

    # Check response status
    if response.status_code != 200:
        return f"HTTP request error status code: {response.status_code}"

    # Use BeautifulSoup to analyze the page's HTML
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(clean_text(response.text), 'html.parser')

    # Extract information from the book
    title = soup.find('h1').text if soup.find('h1') else "Title not found on the page"

    # Category
    category_a = soup.find('ul').find_all('a') if soup.find('ul') else False  # a 1'ul'
    category = category_a[2].text if category_a else "Category not found on the page"

    # Table information
    if soup.find('table'):
        table_td = soup.find('table').find_all('td')
        table = [information.text for information in table_td]
        # UPC
        universal_product_code = table[0] if table else "UPC not found on the page"
        # Price
        price_excluding_tax = table[2] if len(table) >= 2 else "Price_ex not found on the page"
        price_including_tax = table[3] if len(table) >= 3 else "Price_in not found on the page"
        # Number available
        if len(table) >= 5:
            number_available = table[5].split('(')[-1].split(' ')[0]
        else:
            number_available = "number_available not found on the page"

    # image_url
    if soup.find('div', class_='item active'):
        div_img = soup.find('div', class_='item active').find('img')
        image_url = BASE_URL + div_img['src']
    else:
        image_url = "image_url not found on the page"

    # Review rating
    p_star = soup.find('p', class_='star-rating')
    review_rating = p_star['class'][1] if p_star else "Review rating not found on the page"

    # Description
    description_ar = soup.find('article', class_='product_page')
    if description_ar:
        description_p = description_ar.find('p', recursive=False)
        description = description_p.text if description_p else 'Description not found on the page'

    # Summary of book scraper information
    book_data = {"title": title,
                 "category": category,
                 "universal_product_code": universal_product_code,
                 "product_page_url": url,
                 'image_url': image_url,
                 "price_excluding_tax": price_excluding_tax,
                 'price_including_tax': price_including_tax,
                 "number_available": number_available,
                 "review_rating": review_rating,
                 "product_description": description
                 }
    return book_data


# Function to save scraper data in a CSV file
def save_data(data):
    global download_folder

    # Create save folders
    download_folder = Path.cwd() / 'all_book_categories' / category / 'images_of_books'
    download_folder.mkdir(exist_ok=True, parents=True)

    # Create CSV file path
    csv_path = download_folder.parent / (category + '.csv')

    # Open CSV file in add mode
    with open(csv_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # # Check if the file is empty, write the headers
        if file.tell() == 0:
            writer.writerow(data.keys())

        # Write book data to CSV file
        writer.writerow(data.values())


# Function for downloading and saving book images
def download_and_save_images(url):
    # Make a GET request to obtain the image
    response = session.get(url)
    filename = clean_title(title) + '.jpg'
    image_path = download_folder / filename

    # Check if the image exists in the folder
    if image_path.exists():
        return

    # Check response status
    if response.status_code != 200:
        return f'Error status code {response.status_code}'

    # Save image in folder
    with open(image_path, 'wb') as file:
        file.write(response.content)


# close the HTTP request session
session.close()

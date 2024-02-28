import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from my_library import BASE_URL, clean_text, clean_title

# Create a session to manage HTTP requests
session = requests.session()


# Function to extract data from a book
def scrap_book_data(url):
    global category, title

    # Make a GET request to the book URL
    response = session.get(url)
    response.encoding = response.apparent_encoding

    # Check response status
    if response.status_code != 200:
        return f"HTTP request error status code: {response.status_code}"

    # Use BeautifulSoup to analyze the page's HTML
    soup = BeautifulSoup(clean_text(response.text), 'html.parser')  # (lxml-xml, html5lib)

    # Extract information from the book
    title = soup.find('h1').text

    # Category
    category_a = soup.find('ul').find_all('a')  # a single 'ul' in html
    category = category_a[2].text

    # UPC
    table_td = soup.find('table').find_all('td')
    info_table = [information.text for information in table_td]
    universal_product_code = info_table[0]

    # PRICE
    price_excluding_tax = info_table[2]
    price_including_tax = info_table[3]

    # Number available
    number_available = info_table[5].split('(')[-1].split(' ')[0]

    # image_url
    div_img = soup.find('div', class_='item active').find('img')
    image_url = BASE_URL + div_img['src']

    # Review rating
    p_star = soup.find('p', class_='star-rating')
    review_rating = p_star['class'][1]

    # Description
    product_description_p = soup.find('article', class_='product_page').find('p', recursive=False)
    product_description = product_description_p.text if product_description_p else ''

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
                 "product_description": product_description
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
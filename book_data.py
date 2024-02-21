# Import the necessary packages
import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from my_library import *


def scrap_book_information(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    if response.status_code != 200:
        return f"Error status code: {response.status_code}"
    soup = BeautifulSoup(clean_text(response.text), 'html.parser')  # (lxml-xml, html5lib)

    # Title
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
    product_description = soup.find('article', class_='product_page').find('p', recursive=False).text

    # Summary of book scraper information
    book_information = {"title": title,
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

    return book_information


# Save scraper information in a CSV file
def save_data(data):
    if Path('book_information.csv').exists():
        with open('book_information.csv', "a", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow([information for information in data.values()])
    else:
        with open('book_information.csv', "w", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerows([[header for header in data],
                                 [information for information in data.values()]])



# Call the function for a product page url
#book_data = scrap_book_information("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")
#print(type(book_data))


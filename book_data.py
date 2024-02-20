# Import the necessary packages
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"


def clean_text(text):
    return text.replace('\n', '').replace('£', '').replace('../', '')


"""def book_url_scraper(url):
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        return f"Error status code {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    return [CATALOGUE_URL + clean_text(url.find("a")["href"]) for url in soup.find_all('h3')]
"""


def book_information_scraper(url):
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error status code {response.status_code}"
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')  # (lxml-xml, html5lib)

    # Title
    title = soup.find('h1').text

    # Category
    div_page_inner = soup.find_all('div', class_='page_inner')
    li = div_page_inner[1].find('ul').find_all('li')
    category = clean_text(li[2].text)

    # UPC, Price and Availability
    table_td = soup.find('table').find_all('td')
    info_table = [clean_text(information.text) for information in table_td]
    universal_product_code = info_table[0]
    price_excluding_tax = info_table[2]
    price_including_tax = info_table[3]
    number_available = info_table[5].split('(')[1].split(' ')[0]

    # Image URL
    image_src = soup.find('img')['src']
    image_url = clean_text(BASE_URL + image_src)

    # Description
    article_product_page = soup.find('article', class_='product_page').find('p', recursive=False)
    product_description = article_product_page.text

    # image_url
    div_image = soup.find('div', class_='item active').find('img')
    image_url = BASE_URL + clean_text(div_image['src'])

    # Review rating
    p_star = soup.find('p', class_='star-rating')
    review_rating = p_star['class'][1]

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

    with open("book_information.csv", "w", newline='') as file:
        csv.writer(file).writerows([[information for information in book_information],
                             [information for information in book_information.values()]])

    return book_information


# Call the function for a product page url
#print(book_url_scraper(url)[0])
url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
print(book_information_scraper(url))



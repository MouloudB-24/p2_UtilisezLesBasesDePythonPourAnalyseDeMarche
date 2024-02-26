from my_library import *
import csv
from pathlib import Path
import string


def clean_title(title):
    # Delete content between brackets
    title = title.split('(')[0]

    # Filter special characters
    title = ''.join(char for char in title if char not in string.punctuation)

    # `Replace spaces with underscores
    title = title.strip().replace(' ', '_')
    return title


# Scrape book data
def scrap_book_data(url):
    global category, title

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


# Save scraper data in a CSV file
def save_data(data):
    global download_folder

    download_folder = Path.cwd() / 'all_book_categories' / category / 'images_of_books'
    download_folder.mkdir(exist_ok=True, parents=True)

    csv_path = download_folder.parent / (category + '.csv')

    with open(csv_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        if file.tell() == 0:
            # The file is empty, write the headers
            writer.writerow(data.keys())
        writer.writerow(data.values())


# Download and save book images
def download_and_save_images(url):
    response = requests.get(url)
    filename = clean_title(title) + '.jpg'

    if response.status_code != 200:
        return f'Error status code {response.status_code}'

    with open(download_folder / filename, 'wb') as file:
        file.write(response.content)


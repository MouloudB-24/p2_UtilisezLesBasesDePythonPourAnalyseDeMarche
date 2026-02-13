
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
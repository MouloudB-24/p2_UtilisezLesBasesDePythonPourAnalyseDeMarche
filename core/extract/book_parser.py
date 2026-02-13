from bs4 import BeautifulSoup


class BookScrapingError(Exception):
    """
    Error during book scraping
    """
    pass


# Function for scrapping raw book data
def parse_book_data(soup: BeautifulSoup) -> dict: 
    """
    Parse book information from HTML soup.

    :param soup: BeautifulSoup object representing the page's HTML.
    :return: The dictionary containing raw book data.
    """
    # Title
    title_tag = soup.find('h1')
    if not title_tag:
        raise BookScrapingError("Title not found")
    title = title_tag.text      

    # Category
    breadcrumb = soup.find('ul', class_="breadcrumb")
    if not breadcrumb:
        raise BookScrapingError("Category breadcrumb not found")
    category_links = breadcrumb.find_all("a")
    if len(category_links) < 3:
        raise BookScrapingError("Category link not found")
    category = category_links[2].text

    # Table information (obligatoire)
    table = soup.find('table')
    if not table:
        raise BookScrapingError("Product table not found")

    table_td = table.find_all('td')
    if len(table_td) < 6:
        raise BookScrapingError(f"Incomplete table: expected 6+ cells, found {len(table_td)}")

    # UPC
    universal_product_code = table_td[0].text
    # Price
    price_excluding_tax = table_td[2].text
    price_including_tax = table_td[3].text
    # Number available
    number_available = table_td[5].text.split('(')[-1].split(' ')[0]

    # Image URL (obligatoire)
    image_div = soup.find('div', class_='item active')
    if not image_div:
        raise BookScrapingError("Image container not found")

    image_tag = image_div.find('img')
    if not image_tag or 'src' not in image_tag.attrs:
        raise BookScrapingError("Image src not found")

    image_relative_url = image_tag['src']

    # Review rating (obligatoire)
    p_star = soup.find('p', class_='star-rating')
    if not p_star or len(p_star.get('class', [])) < 2:
        raise BookScrapingError("Review rating not found")

    review_rating = p_star['class'][1]

    # Description (optionnel - None si absent)
    description = None
    description_ar = soup.find('article', class_='product_page')
    if description_ar:
        description_p = description_ar.find('p', recursive=False)
        if description_p:
            description = description_p.text
            
    # Summary of book scraper information
    raw_book_data = {"title": title,
                     "category": category,
                     "universal_product_code": universal_product_code,
                     'image_relative_url': image_relative_url,
                     "price_excluding_tax": price_excluding_tax,
                     'price_including_tax': price_including_tax,
                     "number_available": number_available,
                     "review_rating": review_rating,
                     "product_description": description}
    return raw_book_data

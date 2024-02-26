from my_library import *
from urllib.parse import urljoin


def scrap_book_urls(url):
    urls_of_books = []
    while True:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error status code {response.status_code}"

        soup = BeautifulSoup(clean_text(response.text), "html.parser")

        # Pagination
        title_h3 = soup.find_all("h3")
        link_a = [link.find('a')["href"] for link in title_h3]

        urls_of_books.extend([BASE_URL + "catalogue/" + link for link in link_a])

        next_page_element = soup.find('li', class_="next")

        if not next_page_element:
            break

        next_page = next_page_element.find('a')
        next_page_url = next_page.get('href')

        url = urljoin(url, next_page_url)

    return urls_of_books


#print(scrap_book_urls("https://books.toscrape.com/catalogue/category/books/art_25/index.html"))
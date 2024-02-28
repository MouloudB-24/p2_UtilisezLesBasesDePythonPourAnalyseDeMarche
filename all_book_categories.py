import requests
from bs4 import BeautifulSoup

from my_library import BASE_URL


# Function for retrieves all URLs of book categories
def scrap_category_urls(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    # Check response status
    if response.status_code != 200:
        return f"HTTP request error status code: {response.status_code}"

    # Use BeautifulSoup to analyze the page's HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract book category URLs
    div_category = soup.find('div', class_='side_categories').find('ul', class_='nav nav-list')
    li_category = div_category.find('ul').find_all('li')
    urls_of_categories = [BASE_URL + li.find('a')['href'] for li in li_category]

    return urls_of_categories

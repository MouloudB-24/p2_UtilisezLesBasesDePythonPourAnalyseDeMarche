from my_library import *


def scrap_category_urls(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    if response.status_code != 200:
        return f"Error status code: {response.status_code}"
    soup = BeautifulSoup(response.text, 'html.parser')

    div_category = soup.find('div', class_='side_categories').find('ul', class_='nav nav-list')
    li_category = div_category.find('ul').find_all('li')
    urls_of_categories = [BASE_URL + li.find('a')['href'] for li in li_category]

    return urls_of_categories


#print(scrap_category_urls("https://books.toscrape.com/index.html"))
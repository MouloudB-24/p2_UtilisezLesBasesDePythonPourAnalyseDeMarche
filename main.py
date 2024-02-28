import time
from tqdm import tqdm

from a_single_book import scrap_book_data, save_data, download_and_save_images
from a_single_book_category import scrap_book_urls
from all_book_categories import scrap_category_urls

# Records the start of performance measurement
start = time.time()


# La fon
def basic_scrapping(url):
    # book data
    book_data = scrap_book_data(url)

    # Save data in a CSV file
    save_data(book_data)

    # Save book image
    download_and_save_images(book_data["image_url"])


while True:
    print("""
    Welcome to the Books to scrapes price monitoring program, please select one of the following options:
        1 → Scraper data from all books
        2 → Scraper data from books in a category
        3 → Scraper data from a single book
        4 → Quit program
          """)
    your_choice = input("Enter your choice 👉: ")

    if your_choice not in ['1', '2', '3', '4']:
        continue

    if your_choice == '4':
        break

    # Scrape all category data
    if your_choice == '1':
        urls_of_category = scrap_category_urls('https://books.toscrape.com')
        n = 1
        for url in urls_of_category:
            print(f'Scraping category {n}/{len(urls_of_category)} ...')
            urls_of_books = scrap_book_urls(url)

            for url in tqdm(urls_of_books):
                basic_scrapping(url)
            n += 1
        break

    url = input("Enter URL 👉: ")

    # Scrape category data
    if your_choice == '2':
        urls_of_books = scrap_book_urls(url)
        n = 1
        for url in urls_of_books:
            basic_scrapping(url)
            time.sleep(1)
            n += 1
        break

    # Scrape book data
    if your_choice == '3':
        basic_scrapping(url)
        break

# Records the end and displays the performance measurement
end = time.time()
print(f'\n End 👏: {end - start}')


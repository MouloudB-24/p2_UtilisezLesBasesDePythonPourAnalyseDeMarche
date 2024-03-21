import time

from a_single_book import get_book_data
from a_single_book_category import get_category_data
from all_book_categories import get_all_data
from my_library import BASE_URL

# Records the start of performance measurement
start = time.time()

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

    # Scrape all category data
    if your_choice == '1':
        get_all_data(BASE_URL)
        break

    # Enter the url of the book's web page (op3) or that of the category (op2)
    url = input("Enter URL 👉: ")

    # Scrape category data
    if your_choice == '2':
        get_category_data(url)
        break

    # Scrape book data
    if your_choice == '3':
        get_book_data(url)
        break

    if your_choice == '4':
        break

# Records the end and displays the performance measurement
end = time.time()
print(f'\n End 👏: {end - start}')

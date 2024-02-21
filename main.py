from a_single_book_category import *
from a_single_book import *
from all_book_categories import *

urls_of_category = scrap_category_urls('https://books.toscrape.com')

book_number = 1
category_number = 1
for url in urls_of_category:
    urls_of_books = scrap_book_urls(url)
    for url in urls_of_books:
        print(f" Category number {category_number} Book number : {book_number}")
        # book data
        book_data = scrap_book_data(url)

        # Save data in a CSV file
        save_data(book_data)

        book_number += 1
    category_number += 1
print(f'\n End')

from category_book_data import *
from book_data import *


category_urls = scrap_book_category("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

# Save book category data
n = 1
for url in category_urls:
    print(f"url: {n}")

    # book data
    book_data = scrap_book_information(url)

    # Save data in a CSV file
    save_data(book_data)

    n += 1
print(f'\n End')

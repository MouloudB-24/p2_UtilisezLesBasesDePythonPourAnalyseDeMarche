import time

from a_single_book_category import get_category_data
from all_book_categories import get_all_data, get_category_urls
from my_library import BASE_URL

# Records the start of performance measurement
start = time.time()

while True:
    print("""
    Welcome to the Books to scrapes price monitoring program, please select one of the following options:
        1 → Scraper data from all books
        2 → Scraper data from books in a category
        3 → Quit program
          """)
    your_choice = input("Enter your choice 👉: ")

    if your_choice not in ['1', '2', '3']:
        print("\nPlease enter a valid option!")
        continue

    if your_choice == '3':
        break

    # Scrape all category data
    if your_choice == '1':
        get_all_data(BASE_URL)
        break

    # Scrape category data
    if your_choice == '2':
        while True:
            url_of_category = input("Please enter the URL of a book category  👉: ")
            if url_of_category not in get_category_urls(BASE_URL):
                print("\nInvalid URL! Please try again.")
                continue
            else:
                get_category_data(url_of_category)
                break
        break

# Records the end and displays the performance measurement
end = time.time()
print(f'\n End 👏: {end - start}')

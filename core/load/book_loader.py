# Function to save scraper data in a CSV file
def save_book_data(clean_data, category, current_folder=Path.cwd()):
    """
    Save book data in a CSV file.

    :param clean_data: Clean book data as a dictionary.
    :param category: The category of the book.
    :param current_folder: The folder where the file CSV will be saved.
    :return: The folder where book images are saved."""

    # Create save folders
    download_folder = current_folder / 'all_book_categories' / category / 'images_of_books'
    download_folder.mkdir(exist_ok=True, parents=True)

    # Create CSV file path
    save_csv_file = download_folder.parent / (category + '.csv')

    # Open CSV file in add mode
    with open(save_csv_file, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # # Check if the file is empty, write the headers
        if file.tell() == 0:
            writer.writerow(clean_data.keys())

        # Write book data to CSV file
        writer.writerow(clean_data.values())

    return download_folder


# Function for downloading and saving book images
def save_book_images(url_of_book_img, title, download_folder, session):
    """
    Saves book images in a specified folder.

    :param url_of_book_img: URL of the book image.
    :param title: The title of the book.
    :param download_folder: The folder where the book images will be saved.
    :return: None
    """

    # Make a GET request to obtain the image
    response = session.get(url_of_book_img)

    save_jpg_file = download_folder / Path(title + '.jpg')

    # Check if the image exists in the folder
    if save_jpg_file.exists():
        return

    # Save image in folder
    with open(save_jpg_file, 'wb') as file:
        file.write(response.content)
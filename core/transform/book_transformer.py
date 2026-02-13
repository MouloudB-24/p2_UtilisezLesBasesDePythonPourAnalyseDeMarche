# Function for cleaning data
def transform_book_data(raw_data):
    """
    Transforms raw book data into clean data.

    :param raw_data: Raw book data as a dictionary.
    :return: Transformed book data as a dictionary.
    """
    clean_book_data = {}
    for keys, value in raw_data.items():
        if keys == "title":
            value = clean_title(value)
        value = clean_text(value)
        clean_book_data[keys] = value
    return clean_book_data

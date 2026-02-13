# Function for cleaning data
import string


def transform_book_data(raw_data: dict) -> dict:
    """
    Transforms raw book data into clean data.

    :param raw_data: Raw book data as a dictionary.
    :return: Transformed book data as a dictionary.
    """
    return {
        "title": _transform_title(raw_data["title"]),
        "category": raw_data["category"].strip(),
        "universal_product_code": raw_data["universal_product_code"].strip(),
        "price_excluding_tax": _transform_price(raw_data["price_excluding_tax"]),
        "price_including_tax": _transform_price(raw_data["price_including_tax"]),
        "number_available": _transform_availability(raw_data["number_available"]),
        "review_rating": _transform_rating(raw_data["review_rating"]),
        "product_description": raw_data["product_description"] or ""
   }


def _transform_title(title: str) -> str:
    """
    Cleans and formats the title.
    """
    title = title.split('(')[0]
    title = ''.join(char for char in title if char not in string.punctuation)
    return title.strip().replace(' ', '_')


def _transform_price(price_str: str) -> float:
    """
    Convert string price to float.
    """
    return float(price_str.replace('£', ''))


def _transform_availability(availability_str: str) -> int:
    """
    Extract the avialable number.
    """
    return int(availability_str.split('(')[-1].split()[0])


def _transform_rating(rating_str: str) -> int:
    """
    Convert string rating to number.
    """
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    if rating_str not in rating_map:
        raise ValueError(f"Invalid rating: {rating_str}")
    
    return rating_map.get(rating_str, 0)
import pytest
import csv
from pathlib import Path

from core.load.data_loader import load_book_data


@pytest.fixture
def book_data():
    """
    Clean book data.
    """
    return {
        "title": "Test_Book",
        "category": "Fiction",
        "universal_product_code": "abc123",
        "price_excluding_tax": 10.99,
        "price_including_tax": 12.99,
        "number_available": 5,
        "review_rating": 4,
        "product_description": "A test book"
    }


def test_load_book_data_creates_file(tmp_path, book_data):
    csv_path = tmp_path / "Fiction" / "Fiction.csv"
    
    load_book_data(book_data, csv_path)
    
    assert csv_path.exists()
    

def test_load_book_data_writes_headers(tmp_path, book_data):
    csv_path = tmp_path / "Fiction" / "Fiction.csv"
    
    load_book_data(book_data, csv_path)
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        assert headers == list(book_data.keys())
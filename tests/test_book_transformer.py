import pytest
from core.transform.book_transformer import BookTransformError, transform_book_data


@pytest.fixture
def raw_book_data():
    return {
    "title": "A Light in the Attic (Paperback)",
    "category": "Poetry",
    "universal_product_code": "a897fe39b1053632",
    "price_excluding_tax": "£51.77",
    "price_including_tax": "£53.74",
    "number_available": "22",
    "review_rating": "Three",
    "product_description": "It's hard to imagine a world without A Light in the Attic."
}


def test_transform_book_data_success(raw_book_data):
    result = transform_book_data(raw_book_data)
    
    assert result["title"] == "A_Light_in_the_Attic"
    assert result["category"] == "Poetry"
    assert result["universal_product_code"] == "a897fe39b1053632"
    assert result["price_excluding_tax"] == 51.77
    assert result["price_including_tax"] == 53.74
    assert result["number_available"] == 22
    assert result["review_rating"] == 3
    assert result["product_description"] == "It's hard to imagine a world without A Light in the Attic."
    

def test_transform_book_data_invalid_price(raw_book_data):
    bad_data = raw_book_data.copy()
    bad_data["price_excluding_tax"] = "not_a_price"
    
    with pytest.raises(BookTransformError, match=f"Invalid price format: not_a_price"):
        transform_book_data(bad_data)
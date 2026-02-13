import pytest
from bs4 import BeautifulSoup
from core.extract.book_parser import parse_book_data, BookScrapingError


@pytest.fixture
def book_html():
    return """
    <html>
        <h1>A Light in the Attic</h1>
        <ul class="breadcrumb">
            <li><a href="#">Home</a></li>
            <li><a href="#">Books</a></li>
            <li><a href="#">Poetry</a></li>
        </ul>
        <table>
            <tr><td>UPC123456789</td></tr>
            <tr><td>Type</td></tr>
            <tr><td>£51.77</td></tr>
            <tr><td>£51.77</td></tr>
            <tr><td>Tax</td></tr>
            <tr><td>In stock (22 available)</td></tr>
        </table>
        <div class="item active">
            <img src="../../media/cache/image.jpg" alt="book">
        </div>
        <p class="star-rating Three"></p>
        <article class="product_page">
            <p>This is the book description.</p>
        </article>
    </html>
    """
    

def test_parse_book_data_success(book_html):
    soup = BeautifulSoup(book_html, "html.parser")
    result = parse_book_data(soup)
    
    assert result["title"] == "A Light in the Attic"
    assert result["category"] == "Poetry"
    assert result["universal_product_code"] == "UPC123456789"
    assert result["price_excluding_tax"] == "£51.77"
    assert result["price_including_tax"] == "£51.77"
    assert result["number_available"] == "22"
    assert result["image_relative_url"] == "../../media/cache/image.jpg"
    assert result["review_rating"] == "Three"
    assert result["product_description"] == "This is the book description."
    

def test_parse_book_data_missing_title():
    html = "<html><body>No title here</body></html>"
    soup = BeautifulSoup(html, "html.parser")
    
    with pytest.raises(BookScrapingError, match="Title not found"):
        parse_book_data(soup)

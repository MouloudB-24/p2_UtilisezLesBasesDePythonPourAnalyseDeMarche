import pytest
from pathlib import Path
from unittest.mock import Mock
from bs4 import BeautifulSoup

from core.use_cases.process_single_book import process_single_book


def test_process_single_book_integration(tmp_path):
    """
    Test integration of process_single_book with mocked HTTP client.
    """
    mock_client = Mock()
    
    fake_html = """
    <html>
        <h1>Test Book Title</h1>
        <ul class="breadcrumb">
            <li><a href="#">Home</a></li>
            <li><a href="#">Books</a></li>
            <li><a href="#">Fiction</a></li>
        </ul>
        <table>
            <tr><td>UPC123456</td></tr>
            <tr><td>Product Type</td></tr>
            <tr><td>£19.99</td></tr>
            <tr><td>£21.99</td></tr>
            <tr><td>Tax</td></tr>
            <tr><td>In stock (15 available)</td></tr>
        </table>
        <div class="item active">
            <img src="../../media/cache/test.jpg" alt="book">
        </div>
        <p class="star-rating Four"></p>
        <article class="product_page">
            <p>This is a test book description.</p>
        </article>
    </html>
    """
    
    # Configurer les retours du mock
    mock_client.get_text.return_value = fake_html
    mock_client.get_bytes.return_value = b"fake_image_data"
    
    book_url = "http://test.example.com/book/test_1000/index.html"
    base_url = "http://test.example.com/"
    output_dir = tmp_path / "books"
    
    # Appeler la fonction
    result = process_single_book(
        book_url=book_url,
        http_client=mock_client,
        base_url=base_url,
        output_dir=output_dir
    )
    
    # Vérifications du dict retourné
    assert result["title"] == "Test_Book_Title"
    assert result["category"] == "Fiction"
    assert result["universal_product_code"] == "UPC123456"
    assert result["price_excluding_tax"] == 19.99
    assert result["price_including_tax"] == 21.99
    assert result["number_available"] == 15
    assert result["review_rating"] == 4
    assert result["product_description"] == "This is a test book description."
    
    # Vérifier que le fichier CSV a été créé
    csv_path = output_dir / "Fiction" / "Fiction.csv"
    assert csv_path.exists()
    
    # Vérifier le contenu du CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Test_Book_Title" in content
        assert "Fiction" in content
    
    # Vérifier que l'image a été téléchargée
    image_path = output_dir / "Fiction" / "images" / "Test_Book_Title.jpg"
    assert image_path.exists()
    
    # Vérifier le contenu de l'image
    with open(image_path, 'rb') as f:
        assert f.read() == b"fake_image_data"
    
    # Vérifier que les bonnes méthodes ont été appelées
    assert mock_client.get_text.call_count == 1
    assert mock_client.get_bytes.call_count == 1
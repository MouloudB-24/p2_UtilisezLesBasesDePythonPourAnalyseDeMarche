import streamlit as st
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from core.services.http_client import HttpClient
from core.extract.book_parser import parse_book_data
from core.transform.book_transformer import transform_book_data
from core.load.data_loader import load_book_data
from core.load.image_downloader import download_image


def process_single_book(book_url: str, http_client: HttpClient, base_url: str, output_dir: Path) -> dict:
    """
    Process download, parse, transform and save.
    
    Args:
        book_url: URL of the book page
        http_client: HTTP client instance
        base_url: Base URL for constructing absolute URLs
        output_dir: Root directory for saving data
    
    Returns:
        Clean book data as dictionary
    """
    # Download HTML
    html = http_client.get_text(book_url)
    
    # Parse
    soup = BeautifulSoup(html, 'html.parser')
    raw_book_data = parse_book_data(soup)
    
    # Construct absolute image URL
    image_url = urljoin(base_url, raw_book_data["image_relative_url"])
    
    # Transform
    clean_book_data = transform_book_data(raw_book_data)
    clean_book_data["image_url"] = image_url
    
    # Save CSV
    category = clean_book_data["category"]
    csv_path = output_dir / category / f"{category}.csv"
    load_book_data(clean_book_data, csv_path)
    
    # Download image
    image_path = output_dir / category / "images" / f"{clean_book_data['title']}.jpg"
    download_image(image_url, image_path, http_client)
    
    return clean_book_data
    

# Example of use
if __name__ == '__main__':
    pass
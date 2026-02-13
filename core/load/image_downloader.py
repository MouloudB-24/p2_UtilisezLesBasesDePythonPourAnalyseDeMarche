from pathlib import Path
from core.services.http_client import HttpClient


# Function for downloading and saving book images
def download_image(image_url: str, destination_path: Path, http_client: HttpClient) -> None:
    """
    Download book images and save in to specified folder.

    :param image_url: URL of the image to download
    :param destination_path: Full path where to save
    :param HTTP client instance for making requests
    """
    
    # Check if the image exists in the folder
    if destination_path.exists():
        return
    
    # Ensure parent directory exists
    destination_path.parent.mkdir(exist_ok=True, parents=True)
    
    # Download image
    image_bytes = http_client.get_bytes(image_url)
     
    # Save image
    with open(destination_path, 'wb') as file:
        file.write(image_bytes)
import csv
from pathlib import Path

# Function to save scraper data in a CSV file
def load_book_data(clean_data: dict, csv_path: Path) -> None:
    """
    Append book data in a CSV file.

    :param clean_data: Clean book data as a dictionary.
    :param csv_path: Full path to CSV file.
    """

    # Create CSV file path
    csv_path.parent.mkdir(exist_ok=True, parents=True)

    # Open CSV file in add mode
    with open(csv_path, "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        # # Check if the file is empty, write the headers
        if file.tell() == 0:
            writer.writerow(clean_data.keys())

        # Write book data to CSV file
        writer.writerow(clean_data.values())
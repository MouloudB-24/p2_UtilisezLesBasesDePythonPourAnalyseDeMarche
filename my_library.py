

BASE_URL = "https://books.toscrape.com/"


def clean_text(text):
    return text.replace('\n', '').replace('£', '').replace('../', '')
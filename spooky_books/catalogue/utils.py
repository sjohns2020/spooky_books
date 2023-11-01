import requests
import hashlib


# Generate isbn for books that dont have one
def generate_pseudo_isbn(title, author):
    raw_id = f"{title}-{author}".encode("utf-8")
    pseudo_isbn = hashlib.sha1(raw_id).hexdigest()[
        :13
    ]  # taking only the first 13 characters
    return f"845-{pseudo_isbn}"


# Get ISBN from Google Books API
def get_isbn(title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{title}+inauthor:{author}",
        "maxResults": 1,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            book_info = data["items"][0]["volumeInfo"]
            if "industryIdentifiers" in book_info:
                for identifier in book_info["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_13":
                        return identifier["identifier"]

    return generate_pseudo_isbn(title, author)


import requests


def get_publication_year(title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{title}+inauthor:{author}",
        "maxResults": 1,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            book_info = data["items"][0]["volumeInfo"]
            publication_date = book_info.get("publishedDate")
            if (
                publication_date
                and len(publication_date) >= 4
                and publication_date[:4].isdigit()
            ):
                # Ensure that the publication year is in the correct format
                return int(publication_date[:4])
    return None


def get_thumbnail_image(title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{title}+inauthor:{author}",
        "maxResults": 1,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            book_info = data["items"][0]["volumeInfo"]
            image_links = book_info.get("imageLinks")
            thumbnail_url = image_links.get("thumbnail") if image_links else None
            return thumbnail_url

    return None

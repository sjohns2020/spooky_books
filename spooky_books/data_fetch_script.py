import requests
import json
import hashlib


def generate_pseudo_isbn(title, author):
    raw_id = f"{title}-{author}".encode("utf-8")
    pseudo_isbn = hashlib.sha1(raw_id).hexdigest()[
        :13
    ]  # taking only the first 13 characters for brevity
    return f"845-{pseudo_isbn}"


# Fetch Data from google Books API
def fetch_horror_books():
    url = "https://www.googleapis.com/books/v1/volumes"

    # Parameters for the API request
    params = {
        "q": "subject:horror",  # search for only horror books
        "maxResults": 40,
        "printType": "books",
        "fields": "items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,volumeInfo/industryIdentifiers,volumeInfo/imageLinks/thumbnail)",
    }

    # Make the request
    response = requests.get(url, params=params)

    # If the request is successful
    if response.status_code == 200:
        return response.json()

    return None


book_data = fetch_horror_books()


# Transforming Horror Book data to fit my models
def transform_to_json(book_data):
    transformed_data = []

    if book_data:
        authors_index = {}
        current_author_id = 1
        current_book_id = 1

        for item in book_data["items"]:
            info = item["volumeInfo"]

            # Process authors
            if "authors" in info:
                for author_name in info["authors"]:
                    if author_name not in authors_index:
                        first_name, *last_name = author_name.split()
                        last_name = " ".join(last_name) if last_name else ""

                        authors_index[author_name] = current_author_id
                        author_data = {
                            "model": "catalogue.Author",
                            "pk": current_author_id,
                            "fields": {
                                "first_name": first_name,
                                "last_name": last_name,
                            },
                        }
                        transformed_data.append(author_data)
                        current_author_id += 1

            # Process book info
            author_id = (
                authors_index.get(info["authors"][0]) if "authors" in info else None
            )
            isbn = None
            if info.get("industryIdentifiers"):
                for identifier in info["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_13":
                        isbn = identifier["identifier"]
                        break

            # If no valid ISBN was found, generate a pseudo-ISBN instead
            if isbn is None and "authors" in info and info["authors"]:
                author_name = info["authors"][0]
                isbn = generate_pseudo_isbn(info["title"], author_name)

            if isbn:
                book_data = {
                    "model": "catalogue.Book",
                    "pk": current_book_id,
                    "fields": {
                        "title": info["title"],
                        "author": author_id,
                        "publication_year": int(info["publishedDate"].split("-")[0]),
                        "ISBN": isbn,
                        "image": info.get("imageLinks", {}).get(
                            "thumbnail", "image.png"
                        ),
                    },
                }
            transformed_data.append(book_data)
            current_book_id += 1

    return transformed_data


# Transform the fetched data
transformed_json_data = transform_to_json(book_data)

# Save JSON Horror Books data to JSON file.


def save_to_json(data, file_path="./seeds.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Save the data to a JSON file
save_to_json(transformed_json_data)

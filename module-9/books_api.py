"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 9.2 - APIs
Author: Eric J. Turman
Date: 2026-08-03
Email: ejturman@my365.bellevue.edu

Description:
------------

Search Open Library and display the raw response followed by readable
summaries of up to three returned volumes.

Notes:
------

Only one HTTP request is made for both raw and formatted output.
"""

# ============================================================================
# Imports
# ============================================================================
from typing import Final, TypedDict

import requests


# ============================================================================
# Constants
# ============================================================================
OPEN_LIBRARY_API_URL: Final[str] = "https://openlibrary.org/search.json"
SEARCH_QUERY: Final[str] = "python programming"
MAX_RESULTS: Final[int] = 3
REQUEST_TIMEOUT_SECONDS: Final[int] = 10
UNKNOWN_VALUE: Final[str] = "Unknown"


# ============================================================================
# Data Structures
# ============================================================================
class BookSummary(TypedDict):
    """Validated values displayed for one Open Library book."""

    title: str
    authors: str
    published_date: str
    page_count: str
    categories: str


# ============================================================================
# Functions
# ============================================================================
def request_books() -> requests.Response:
    """Search Open Library for books.

    Returns
    -------
    requests.Response
        A successful response containing matching books.

    Raises
    ------
    requests.RequestException
        If the request fails or the response has an unsuccessful status.
    """
    parameters: dict[str, str | int] = {
        "q": SEARCH_QUERY,
        "limit": MAX_RESULTS,
    }
    response = requests.get(
        OPEN_LIBRARY_API_URL,
        params=parameters,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    print(f"HTTP status: {response.status_code}")
    response.raise_for_status()
    print(response.text)
    return response


def readable_string(value: object) -> str:
    """Return a nonempty string or the standard missing-value label.

    Parameters
    ----------
    value : object
        External value to validate.

    Returns
    -------
    str
        The validated string or ``UNKNOWN_VALUE``.
    """
    if isinstance(value, str) and value.strip():
        return value
    return UNKNOWN_VALUE


def readable_string_list(value: object) -> str:
    """Join valid strings or return the standard missing-value label.

    Parameters
    ----------
    value : object
        External value expected to contain a list of strings.

    Returns
    -------
    str
        The joined strings or ``UNKNOWN_VALUE``.
    """
    if isinstance(value, list):
        strings = [item for item in value if isinstance(item, str) and item.strip()]
        if strings:
            return ", ".join(strings)
    return UNKNOWN_VALUE


def readable_nonnegative_integer(value: object) -> str:
    """Return a nonnegative integer as text or the missing-value label.

    Parameters
    ----------
    value : object
        External value expected to contain a nonnegative integer.

    Returns
    -------
    str
        The integer as text or ``UNKNOWN_VALUE``.
    """
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return str(value)
    return UNKNOWN_VALUE


def validate_books_data(data: object) -> list[BookSummary]:
    """Validate and narrow the Open Library fields used for display.

    Parameters
    ----------
    data : object
        Parsed JSON data from Open Library.

    Returns
    -------
    list[BookSummary]
        Validated summaries for no more than ``MAX_RESULTS`` books.

    Raises
    ------
    ValueError
        If the required response structure is invalid.
    """
    if not isinstance(data, dict):
        raise ValueError("the books response is not an object")

    documents = data.get("docs", [])
    if not isinstance(documents, list):
        raise ValueError("the books docs value is not a list")

    books: list[BookSummary] = []
    for document in documents[:MAX_RESULTS]:
        if not isinstance(document, dict):
            raise ValueError("a book entry is not an object")

        books.append(
            {
                "title": readable_string(document.get("title")),
                "authors": readable_string_list(document.get("author_name")),
                "published_date": readable_nonnegative_integer(
                    document.get("first_publish_year")
                ),
                "page_count": readable_nonnegative_integer(
                    document.get("number_of_pages_median")
                ),
                "categories": readable_string_list(document.get("subject")),
            }
        )

    return books


def display_books(books: list[BookSummary]) -> None:
    """Display readable summaries for the selected books.

    Parameters
    ----------
    books : list[BookSummary]
        Validated book summaries to display.
    """
    if not books:
        print("No books were found.")
        return

    for number, book in enumerate(books, start=1):
        print(f"\nBook {number}")
        print(f"Title: {book['title']}")
        print(f"Authors: {book['authors']}")
        print(f"Published: {book['published_date']}")
        print(f"Pages: {book['page_count']}")
        print(f"Categories: {book['categories']}")


# ============================================================================
# Main Program Flow
# ============================================================================
def main() -> None:
    """Retrieve, validate, and display Open Library search results."""
    try:
        response = request_books()
        data: object = response.json()
        books = validate_books_data(data)
        display_books(books)
    except requests.Timeout:
        print("Unable to retrieve book data: the request timed out.")
    except requests.ConnectionError:
        print("Unable to retrieve book data: could not connect to the service.")
    except requests.exceptions.JSONDecodeError:
        print("Unable to retrieve book data: the response was not valid JSON.")
    except requests.RequestException as error:
        print(f"Unable to retrieve book data: request failed ({error}).")
    except ValueError as error:
        print(f"Unable to retrieve book data: unexpected response structure ({error}).")


# ============================================================================
# Program Entry Point
# ============================================================================
if __name__ == "__main__":
    main()



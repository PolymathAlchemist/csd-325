"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 9.2 - APIs
Author: Eric J. Turman
Date: 2026-08-03
Email: ejturman@my365.bellevue.edu

Description:
------------

Retrieve live astronaut data and display the reported count and each name
with the literal " - onboard" assignment text.

Notes:
------

The spacecraft name returned by the API is intentionally not displayed.
"""

# ============================================================================
# Imports
# ============================================================================
from typing import Final

import requests


# ============================================================================
# Constants
# ============================================================================
ASTRONAUTS_URL: Final[str] = "http://api.open-notify.org/astros.json"
REQUEST_TIMEOUT_SECONDS: Final[int] = 5


# ============================================================================
# Functions
# ============================================================================
def request_astronaut_data() -> requests.Response:
    """Request astronaut data from Open Notify.

    Returns
    -------
    requests.Response
        A successful response containing astronaut data.

    Raises
    ------
    requests.RequestException
        If the request fails or the response has an unsuccessful status.
    """
    response = requests.get(ASTRONAUTS_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    print(f"HTTP status: {response.status_code}")
    return response


def validate_astronaut_data(data: object) -> tuple[int, list[str]]:
    """Validate the astronaut response fields used by the program.

    Parameters
    ----------
    data : object
        Parsed JSON data from Open Notify.

    Returns
    -------
    tuple[int, list[str]]
        The reported astronaut count and validated astronaut names.

    Raises
    ------
    ValueError
        If the required response structure or values are invalid.
    """
    if not isinstance(data, dict):
        raise ValueError("the astronaut response is not an object")

    count = data.get("number")
    people = data.get("people")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError("the astronaut count is invalid")
    if not isinstance(people, list):
        raise ValueError("the astronaut people value is not a list")

    names: list[str] = []
    for person in people:
        if not isinstance(person, dict):
            raise ValueError("an astronaut entry is not an object")
        name = person.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("an astronaut entry has an invalid name")
        names.append(name)

    return count, names


def display_astronauts(names: list[str]) -> None:
    """Display each astronaut name with the required literal suffix.

    Parameters
    ----------
    names : list[str]
        Validated astronaut names to display.
    """
    for name in names:
        print(f"{name} - onboard")


# ============================================================================
# Main Program Flow
# ============================================================================
def main() -> None:
    """Retrieve, validate, and display the current astronaut data."""
    try:
        response = request_astronaut_data()
        data: object = response.json()
        count, names = validate_astronaut_data(data)
        print(f"Astronaut count: {count}")
        display_astronauts(names)
    except requests.Timeout:
        print("Unable to retrieve astronaut data: the request timed out.")
    except requests.ConnectionError:
        print("Unable to retrieve astronaut data: could not connect to the service.")
    except requests.exceptions.JSONDecodeError:
        print("Unable to retrieve astronaut data: the response was not valid JSON.")
    except requests.RequestException as error:
        print(f"Unable to retrieve astronaut data: request failed ({error}).")
    except ValueError as error:
        print(f"Unable to retrieve astronaut data: unexpected response structure ({error}).")


# ============================================================================
# Program Entry Point
# ============================================================================
if __name__ == "__main__":
    main()


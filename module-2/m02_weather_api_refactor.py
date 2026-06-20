"""
CIS245-T303 Introduction to Programming
Instructor: Dr. Sasan Azazian
Assignment: M11: Assignment Part II - Weather API Program
Author: Eric J. Turman
Date: 2025-11-22
Email: ejturman@my365.bellevue.edu

The program prompts the user for their ZIP code,
requests weather forecast data from openweathermap.org, and
allows the user to try again multiple times.
Using the program developed in Module 11: Part I,
this program refines the output by parsing the JSON response.
It displays at least two of the weather-related attributes from the
"main" object in the JSON response.

This program actually displays up to Four if available:
    * City
    * Temperature
    * Feels like temperature
    * Humidity

The program emphasizes robust input validation using
regular expressions and validation from an open-source
API ZIP code database, modular design with reusable functions, and
clear documentation practices using NumPy docstring notation.

Note:
-----
This has been refactored to put into practice some of the lessons that I have
learned from the Pragmatic Programmer. The old version was already DRY, but I
did not know how to apply orthogonality as well as I understand it now.
In particular get_data() needed some attention in that regard.
"""

import difflib
import json
import re
import subprocess
import sys
import textwrap
from collections.abc import Collection
from typing import (
    Any,
    Final,
    overload,
)

# ========================================================================
# Named Constants
# ========================================================================
INTRO_MESSAGE: Final[str] = (
    "Welcome to the 'Whether' report!\nI'll provide you a weather report "
    f"depending on whether you give me\na valid ZIP code.\n{'~' * 79}"
)

EXIT_MESSAGE: Final[str] = (
    f"{'-' * 79}\nThank you! Please come again."
)

ZIP_CODE_INPUT = "Please enter a 5-digit ZIP code: "

ZIP_CODE_RE: Final[re.Pattern[str]] = re.compile(r"^\d{5}$")

ZIP_CODE_ERROR: str = "ZIP code is not valid. Must be ONLY 5 numbers"

CONTINUE_INPUT: Final[str] = "See another weather report? (y/yes, n/no): "

YES_NO_RE: Final[re.Pattern[str]] = re.compile(r"^(?:y|yes|n|no)$",
                                               re.IGNORECASE)

YES_NO_ERROR: Final[str] = "Only y, yes, n, no are accepted."

WEATHER_API_KEY: Final[str] = "906b6939735602a519447e37a839d229"

WEATHER_BASE_URL: Final[str] = (
    "https://api.openweathermap.org/data/2.5/weather"
)

NA_INPUT_VALUE: Final[str] = "NA"

LIST_OPTIONS_COMMAND: Final[str] = "L"


# ========================================================================
# Input Validation Function Overloads
# ========================================================================
@overload
def get_data(
        input_message: str,
        match_pattern: re.Pattern[str],
        error_message: str,
        allow_blank_as_na: bool = False,
        *,
        list_options_command: str | None = LIST_OPTIONS_COMMAND
) -> str:
    ...


@overload
def get_data(
        input_message: str,
        match_pattern: Collection[str],
        error_message: str,
        allow_blank_as_na: bool = False,
        *,
        list_options_command: str | None = LIST_OPTIONS_COMMAND
) -> str:
    ...


@overload
def get_data(
        input_message: str,
        match_pattern: dict[str, Any],
        error_message: str,
        allow_blank_as_na: bool = False,
        *,
        list_options_command: str | None = LIST_OPTIONS_COMMAND
) -> str:
    ...


# ========================================================================
# Input Validation Helper Functions
# ========================================================================
def print_input_error(error_message: str) -> None:
    """
    Print a formatted input-validation error message.

    Parameters
    ----------
    error_message : str
        Message explaining what was wrong with the user's input.

    Returns
    -------
    None
    """
    print(textwrap.fill(
        f"{'!' * 79}\n{error_message}\n{'!' * 79}",
        width=79
    ))


def is_string_collection(possible_values: Collection[str]) -> bool:
    """
    Check whether all items in a collection are strings.

    Parameters
    ----------
    possible_values : Collection[str]
        Collection to inspect.

    Returns
    -------
    bool
        True if every item is a string, otherwise False.
    """
    return all(isinstance(item, str) for item in possible_values)


def confirm_fuzzy_match(close_match: str) -> bool:
    """
    Ask the user whether a suggested fuzzy match should be accepted.

    Parameters
    ----------
    close_match : str
        Suggested replacement value.

    Returns
    -------
    bool
        True if the user answers yes, otherwise False.
    """
    while True:
        answer = input(f"Did you mean '{close_match}'?").strip()
        if YES_NO_RE.fullmatch(answer):
            return answer.upper()[0] == "Y"
        print_input_error(YES_NO_ERROR)


def get_allowed_values(
        match_pattern: Collection[str] | dict[str, Any]
) -> list[str]:
    """
    Convert supported list-style validation patterns to a list of strings.

    Parameters
    ----------
    match_pattern : Collection[str] | dict[str, Any]
        A collection of allowed strings or a dictionary whose keys are
        allowed input strings.

    Returns
    -------
    list[str]
        Allowed input values.

    Raises
    ------
    TypeError
        If match_pattern is not a collection of strings or a dictionary.
    """
    if isinstance(match_pattern, dict):
        return list(match_pattern.keys())

    if (
            isinstance(match_pattern, Collection)
            and not isinstance(match_pattern, str)
            and is_string_collection(match_pattern)
    ):
        return list(match_pattern)

    raise TypeError(
        "match_pattern must be a regular expression pattern, a "
        "collection of strings, or a dictionary with string keys."
    )


# ========================================================================
# Input Validation Implementation
# ========================================================================
def get_data(
        input_message: str,
        match_pattern: re.Pattern[str] | Collection[str] | dict[str, Any],
        error_message: str,
        allow_blank_as_na: bool = False,
        *,
        list_options_command: str | None = LIST_OPTIONS_COMMAND
) -> str:
    """
    Prompt for input until the user enters a valid value.

    This reusable validation helper supports three validation patterns:
    regular expressions, collections of allowed strings, and dictionaries
    whose keys are allowed strings. Collection and dictionary validation
    also supports fuzzy-match suggestions.

    Parameters
    ----------
    input_message : str
        Prompt shown to the user.
    match_pattern : re.Pattern[str] | Collection[str] | dict[str, Any]
        Validation rule. A regular expression must fully match the input.
        A collection must contain only valid string responses. A dictionary
        uses its keys as the valid string responses.
    error_message : str
        Message displayed when the user enters invalid input.
    allow_blank_as_na : bool, optional
        If True, return "NA" when the user enters an empty string or "NA".
        The default is False.
    list_options_command : str | None, optional
        Command that prints all valid options for collection or dictionary
        validation. The default is "L". Use None to disable this behavior.

    Returns
    -------
    str
        The validated input value, the accepted fuzzy-match value, or "NA"
        when allow_blank_as_na is True and the user enters a blank or "NA".

    Raises
    ------
    TypeError
        If match_pattern is not a regular expression, a collection of
        strings, or a dictionary.

    Notes
    -----
    Fuzzy matching is attempted only for collection and dictionary
    validation. When a close match is found, the user is asked whether to
    accept it. A yes answer returns the suggested value; a no answer
    restarts the prompt.
    """
    while True:
        value: str = input(input_message).strip()
        if allow_blank_as_na and value.upper() in ("", NA_INPUT_VALUE):
            return NA_INPUT_VALUE

        # ----------------------------------------------------------------
        # Case 1: Regular Expression
        # ----------------------------------------------------------------
        if isinstance(match_pattern, re.Pattern):
            if match_pattern.fullmatch(value):
                return value
            print_input_error(error_message)
            continue

        # ----------------------------------------------------------------
        # Case 2 and 3: Collection of Strings or Dictionary Keys
        # ----------------------------------------------------------------
        try:
            allowed_values = get_allowed_values(match_pattern)
        except TypeError:
            raise TypeError(
                "match_pattern must be a regular expression pattern, a "
                "collection of strings, or a dictionary with string keys."
            ) from None

        if (
                list_options_command is not None
                and value.upper() == list_options_command.upper()
        ):
            valid_input_message = ", ".join(allowed_values)
            print(textwrap.fill(valid_input_message, width=79))
            continue

        if value in allowed_values:
            return value

        close_matches = difflib.get_close_matches(
            value,
            allowed_values,
            n=1
        )
        if close_matches:
            if confirm_fuzzy_match(close_matches[0]):
                return close_matches[0]
            continue

        print_input_error(error_message)


def ensure_requests_installed():
    """
        Ensure the 'requests' module is installed.
            If not available, install it using pip, then import it. This
            protects against unnecessary reimports.
            This will make static code analyzers unhappy,
            but this is a well-known module and should be safe.
        Returns:
        module
            the imported 'requests' module
        """
    try:
        import requests
        return requests
    except ImportError:
        print(
            "The 'requests' module is not installed. "
            "Attempting installation..."
        )
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "requests"]
            )
            print("Successfully installed 'requests'.")
            import requests
            return requests
        except Exception as error:
            print("Failed to install 'requests'.")
            print("Error:", error)
            sys.exit(1)


# Call the function and bind the returned module in global scope
requests = ensure_requests_installed()


def is_valid_zip_code(zip_code: str) -> bool:
    """
    Validate a 5-digit US ZIP code by querying the Zippopotam.us API.

    Parameters
    ----------
    zip_code : str
        The ZIP code to validate through Zippopotam.us.

    Returns
    -------
    bool
        True if the API responds with HTTP status code 200 (ZIP exists),
        otherwise False.
    """

    if not (zip_code.isdigit() and len(zip_code) == 5):
        return False

    zip_code_url = f"https://api.zippopotam.us/us/{zip_code}"
    response = requests.get(zip_code_url)

    return response.status_code == 200


def get_zip_code() -> str:
    """
    Get a raw ZIP code and check whether it matches the ZIP code
    regex pattern.
    * Checks is_valid_zip_code() to see if it is a registered US ZIP code.
    * Loops until a valid ZIP code is entered.

    Returns
    -------
    str
        The validated ZIP code from Zippopotam.us.
    """
    while True:
        try:
            zip_code_raw = get_data(
                ZIP_CODE_INPUT,
                ZIP_CODE_RE,
                ZIP_CODE_ERROR
            )
            if is_valid_zip_code(zip_code_raw):
                return zip_code_raw
            else:
                raise ValueError("not a valid ZIP code")
        except ValueError as error:
            print(textwrap.fill(
                f"{'!' * 79}\n{error}\n{'!' * 79}",
                width=79
            ))


def get_weather(zip_code: str) -> dict[str, Any]:
    """
    Given a ZIP code, get the weather from the API.

    Parameters
    ----------
    zip_code: str
        a valid US ZIP code

    Returns
    -------
    dict[str, Any]
        The parsed JSON weather data from the API
    """
    weather_url = (
        f"{WEATHER_BASE_URL}?"
        f"zip={zip_code},us&"
        f"units=imperial&"
        f"APPID={WEATHER_API_KEY}"
    )
    response = requests.get(weather_url)

    if response.status_code != 200:
        raise ValueError(
            f"Failed to get weather data for ZIP code '{zip_code}'"
        )

    try:
        return response.json()
    except json.JSONDecodeError as error:
        raise ValueError("Received invalid JSON from weather API.") from error


def display_weather(weather_data: dict[str, Any]) -> None:
    """
    Display selected weather information from the API response.

    Parameters
    ----------
    weather_data : dict[str, Any]
        Parsed JSON data returned by the weather API.

    Returns
    -------
    None
    """
    main_section = weather_data.get("main", {})
    temperature = main_section.get("temp")
    feels_like = main_section.get("feels_like")
    humidity = main_section.get("humidity")
    city_name = weather_data.get("name", "Unknown location")

    print("-" * 79)
    print(f"Weather report for: {city_name}")
    if temperature is not None:
        print(f"      Temperature : {temperature:.1f}°F")
    if feels_like is not None:
        print(f"      Feels like  : {feels_like:.1f}°F")
    if humidity is not None:
        print(f"      Humidity    : {humidity}%")
    print("-" * 79)


def main() -> None:
    """
    Entry point for the program.
        * Asks user for a valid ZIP code.
        * Requests weather from the API.
        * Displays formatted weather information from the API.
        * Asks user if they want to enter another ZIP code.
        * Loops until user wants to stop

    Returns
    -------
    None
    """
    print(INTRO_MESSAGE)
    while True:
        zip_code = get_zip_code()
        try:
            weather_report = get_weather(zip_code)
        except ValueError as error:
            print(textwrap.fill(
                f"{'!' * 79}\n{error}\n{'!' * 79}",
                width=79
            ))
        else:
            display_weather(weather_report)

        again = get_data(
            CONTINUE_INPUT,
            YES_NO_RE,
            YES_NO_ERROR
        )
        if again.upper()[0] == "N":
            break
        else:
            print(f"{'+' * 79}")
    print(EXIT_MESSAGE)


if __name__ == "__main__":
    main()

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


# ========================================================================
# Logic Functions
# ========================================================================
@overload
def get_data(
        input_message: str,
        match_pattern: re.Pattern[str],
        error_message: str,
        na: bool = False
) -> str:
    ...


@overload
def get_data(
        input_message: str,
        match_pattern: Collection[str],
        error_message: str,
        na: bool = False
) -> str:
    ...


@overload
def get_data(
        input_message: str,
        match_pattern: dict[str, Any],
        error_message: str,
        na: bool = False
) -> str:
    ...


def get_data(
        input_message: str,
        match_pattern: re.Pattern[str] | Collection[str] | dict[str, Any],
        error_message: str,
        na: bool = False
) -> str:
    """
    Get information is a modular input validation function that supports
    three kinds of validation patterns to ensure safe and correct
    user input.
    * Case 1: Regular expressions (re.Pattern)
        - Input must match the regex pattern
    * Case 2: Collection of strings (Collection[str])
        - Input matched against a whitelist of strings.
        - Suggests a fuzzy match against a whitelist of strings.
    * Case 3: Dictionary of string keys (dict[str,Any])
        - Input matched against a whitelist of dictionary keys.
        - Suggests a fuzzy match against a whitelist of dictionary keys.

    Parameters
    ----------
    input_message: str
        Let the user know what information to type in.
    match_pattern: Overloaded parameter:
        re.Pattern[str] | Collection[str] | dict[str,Any]
    error_message
        Message to let the user know what they are typing wrong.
    na: bool
        If True, return "NA" instead of raising an error if
        an empty string or "NA" is entered.
    Returns
    -------
    str
        Validated input string value.
    Raises
    -------
    TypeError
        If match_pattern is not a supported type.
    RunTimeError if the function reaches an
        unexpected state (which should be impossible).
    Notes
    -------
    This function will loop until it receives a valid input
    """
    while True:
        value: str = input(input_message).strip()
        if na and (value.lower() == "na" or value.lower() == ""):
            return "NA"

        # ----------------------------------------------------------------
        # Case 1: Regular Expression
        # ----------------------------------------------------------------
        if isinstance(match_pattern, re.Pattern):
            try:
                if not match_pattern.fullmatch(value):
                    raise ValueError(error_message)
                return value
            except ValueError as error:
                print(textwrap.fill(
                    f"{'!' * 79}\n{error}\n{'!' * 79}",
                    width=79
                ))

        # ----------------------------------------------------------------
        # Case 2: Collection of Strings
        # ----------------------------------------------------------------
        elif (
                isinstance(match_pattern, Collection)
                and not isinstance(match_pattern, dict)
                and not isinstance(match_pattern, str)
                and all(isinstance(item, str) for item in match_pattern
                        )):
            if value.upper() == "L":
                valid_input_message = ", ".join(match_pattern)
                print(textwrap.fill(valid_input_message, width=79))
                continue
            else:
                try:
                    if value in match_pattern:
                        return value
                    close_matches = difflib.get_close_matches(
                        value,
                        match_pattern,
                        n=1
                    )
                    if close_matches:
                        use_close = get_data(
                            f"Did you mean '{close_matches[0]}'?",
                            YES_NO_RE,
                            YES_NO_ERROR
                        )
                        if use_close[0].upper() == "Y":
                            return close_matches[0]
                        else:
                            continue
                    raise ValueError(error_message)
                except ValueError as error:
                    print(textwrap.fill(
                        f"{'!' * 79}\n{error}\n{'!' * 79}",
                        width=79
                    ))

        # ----------------------------------------------------------------
        # Case 3: Dictionary
        # ----------------------------------------------------------------
        elif isinstance(match_pattern, dict):
            valid_keys = list(match_pattern.keys())
            if value.upper() == "L":
                valid_input_message = ", ".join(valid_keys)
                print(textwrap.fill(valid_input_message, width=79))
                continue
            else:
                try:
                    if value in valid_keys:
                        return value
                    close_matches = difflib.get_close_matches(
                        value,
                        valid_keys,
                        n=1
                    )
                    if close_matches:
                        use_close = get_data(
                            f"Did you mean '{close_matches[0]}'?",
                            YES_NO_RE,
                            YES_NO_ERROR
                        )
                        if use_close[0].upper() == "Y":
                            return close_matches[0]
                        else:
                            continue
                    raise ValueError(error_message)
                except ValueError as error:
                    print(textwrap.fill(
                        f"{'!' * 79}\n{error}\n{'!' * 79}",
                        width=79
                    ))

        # ----------------------------------------------------------------
        # Fall-through Case: Unexpected match_pattern
        # ----------------------------------------------------------------
        else:
            raise TypeError(
                "match_pattern must be a regular expression pattern, a "
                "collection of strings, or a dictionary with string keys."
            )
    raise RuntimeError("get_data() reached an unexpected state")


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

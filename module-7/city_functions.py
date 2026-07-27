"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 7.2 - Test Cases
Author: Eric J. Turman
Date: 2026-07-25
Email: ejturman@my365.bellevue.edu

Description:
------------

Format city and country names for display.

Notes:
------

This stage implements the initial two-parameter version of the city-country
formatting function.
"""


def city_country(
    city_name: str,
    country_name: str,
    population: int | None = None,
    language: str | None = None,
) -> str:
    """Format a city and country name for display.

    Parameters
    ----------
    city_name
        Name of the city.
    country_name
        Name of the country.
    population
        Optional population of the city.
    language
        Optional language spoken in the city.

    Returns
    -------
    str
        The city and country, with population and language when provided,
        formatted for display.
    """
    formatted_location = f"{city_name}, {country_name}"

    if population is not None:
        formatted_location = f"{formatted_location} - population {population}"

    if language is not None:
        formatted_location = f"{formatted_location}, {language}"

    return formatted_location


def main() -> None:
    """Run the city-country formatting demonstration."""
    print(city_country("Santiago", "Chile"))
    print(
        city_country(
            "Tokyo",
            "Japan",
            13960000,
        )
    )
    print(
        city_country(
            "Reykjavik",
            "Iceland",
            140000,
            "Icelandic",
        )
    )


if __name__ == "__main__":
    main()

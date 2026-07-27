"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 7.2 - Test Cases
Author: Eric J. Turman
Date: 2026-07-26
Email: ejturman@my365.bellevue.edu

## Description:

Initial unit tests for the city_country() function.

## Notes:

Stage 2 verifies the original two-parameter implementation.
"""

import unittest

from city_functions import city_country


class CityCountryTestCase(unittest.TestCase):
    """Tests for city and country name formatting."""

    def test_city_country(self) -> None:
        """Verify city and country names are formatted correctly."""
        formatted_location = city_country("Santiago", "Chile")
        self.assertEqual(formatted_location, "Santiago, Chile")


if __name__ == "__main__":
    unittest.main()

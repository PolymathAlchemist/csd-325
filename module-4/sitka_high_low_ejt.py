"""
CSD325-T301 Advanced Python
Instructor: Professor Sloan
Assignment: Module 4.2 - High/Low Temperatures
Author: Eric J. Turman
Date: 2026-07-05
Email: ejturman@my365.bellevue.edu

Original program provided as course material.
Modified by Eric J. Turman to:
- Add an interactive menu.
- Display either daily high or low temperatures.
- Allow repeated selections until the user exits.
- Improve documentation and program organization.
"""


import csv
from datetime import datetime
from pathlib import Path

from matplotlib import pyplot as plt


# ============================================================================
# Constants
# ============================================================================

DATA_FILE: str = "sitka_weather_2018_simple.csv"


# ============================================================================
# Functions
# ============================================================================

def display_menu() -> None:
    """
    Display the Sitka Weather Viewer menu.

    Returns
    -------
    None
    """
    print("\n==========================")
    print(" Sitka Weather Viewer")
    print("==========================")
    print("1. High Temperatures")
    print("2. Low Temperatures")
    print("3. Exit")


def load_weather_data() -> tuple[list[datetime], list[int], list[int]]:
    """
    Load dates, high temperatures, and low temperatures from the CSV file.

    Returns
    -------
    tuple[list[datetime], list[int], list[int]]
        Lists containing dates, daily high temperatures, and daily low
        temperatures. Empty lists are returned if the file cannot be loaded.
    """
    dates: list[datetime] = []
    highs: list[int] = []
    lows: list[int] = []
    file_path = Path(__file__).with_name(DATA_FILE)

    try:
        with file_path.open() as file_object:
            reader = csv.reader(file_object)
            next(reader)

            for row_number, row in enumerate(reader, start=2):
                try:
                    current_date = datetime.strptime(row[2], "%Y-%m-%d")
                    high_temperature = int(row[5])
                    low_temperature = int(row[6])
                except IndexError as error:
                    raise ValueError(
                        f"Missing data in row {row_number}."
                    ) from error
                except ValueError as error:
                    raise ValueError(
                        f"Invalid date or temperature data in row "
                        f"{row_number}."
                    ) from error

                dates.append(current_date)
                highs.append(high_temperature)
                lows.append(low_temperature)
    except FileNotFoundError:
        print(f"Error: The weather data file '{DATA_FILE}' was not found.")
    except ValueError as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"An unexpected error occurred while loading data: {error}")

    return dates, highs, lows


def plot_temperatures(
    dates: list[datetime],
    temperatures: list[int],
    color: str,
    title: str,
) -> None:
    """
    Plot daily temperatures for Sitka.

    Parameters
    ----------
    dates : list[datetime]
        Dates to display on the x-axis.
    temperatures : list[int]
        Temperature values to display on the y-axis.
    color : str
        Matplotlib color used for the plotted line.
    title : str
        Title displayed above the graph.

    Returns
    -------
    None
    """
    try:
        fig, ax = plt.subplots()
        ax.plot(dates, temperatures, c=color)

        plt.title(title, fontsize=24)
        plt.xlabel("", fontsize=16)
        fig.autofmt_xdate()
        plt.ylabel("Temperature (F)", fontsize=16)
        plt.tick_params(axis="both", which="major", labelsize=16)

        print("\nDisplaying graph...")
        print("Close the graph window to return to the menu.\n")
        plt.show()
    except Exception as error:
        print(f"An unexpected error occurred while plotting data: {error}")


def show_high_temperatures(
    dates: list[datetime],
    highs: list[int],
) -> None:
    """
    Display a graph of daily high temperatures.

    Parameters
    ----------
    dates : list[datetime]
        Dates for the plotted high temperatures.
    highs : list[int]
        Daily high temperatures.

    Returns
    -------
    None
    """
    if not dates or not highs:
        print("High temperature data is not available.")
        return

    plot_temperatures(
        dates,
        highs,
        "red",
        "Daily High Temperatures - 2018",
    )


def show_low_temperatures(
    dates: list[datetime],
    lows: list[int],
) -> None:
    """
    Display a graph of daily low temperatures.

    Parameters
    ----------
    dates : list[datetime]
        Dates for the plotted low temperatures.
    lows : list[int]
        Daily low temperatures.

    Returns
    -------
    None
    """
    if not dates or not lows:
        print("Low temperature data is not available.")
        return

    plot_temperatures(
        dates,
        lows,
        "blue",
        "Daily Low Temperatures - 2018",
    )


# ============================================================================
# Main Program
# ============================================================================

def main() -> None:
    """
    Coordinate the application's menu-driven workflow.

    Loads the weather data once and allows the user to
    view high or low temperatures repeatedly until exiting.

    Returns
    -------
    None
    """
    dates, highs, lows = load_weather_data()

    while True:
        display_menu()
        choice = input("Please enter your choice: ")

        if choice == "1":
            show_high_temperatures(dates, highs)
        elif choice == "2":
            show_low_temperatures(dates, lows)
        elif choice == "3":
            print("\nThank you for using the Sitka Weather Viewer.")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"An unexpected error occurred: {error}")

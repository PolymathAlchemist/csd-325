"""
CSD325-T301 Advanced Python
Instructor: Dr. Ed Parks
Assignment: Module 1.3 - 100 Bottles of Beer on the Wall
Author: Eric J. Turman
Date: 2026-06-12
Email: ejturman@my365.bellevue.edu

This program asks the user how many bottles of beer are on the wall,
validates that the response is a whole-number integer within the accepted
range, and then counts down the traditional bottles of beer song until no
bottles remain.
"""

from typing import Final

# ========================================================================
# Named Constants
# ========================================================================

MINIMUM_BOTTLES: Final[int] = 1
MAXIMUM_BOTTLES: Final[int] = 100

TITLE_TEXT: Final[str] = (
    "Welcome to the Bottles of Beer on the Wall countdown!\n"
    "Enter a starting number, and the program will count down from there."
)

BOTTLE_PROMPT: Final[str] = (
    f"How many bottles of beer are on the wall "
    f"({MINIMUM_BOTTLES}-{MAXIMUM_BOTTLES})? "
)

INTEGER_ERROR_MESSAGE: Final[str] = (
    "Please enter a whole-number integer."
)

RANGE_ERROR_MESSAGE: Final[str] = (
    f"Please enter a number from {MINIMUM_BOTTLES} to {MAXIMUM_BOTTLES}."
)

REMINDER_MESSAGE: Final[str] = (
    "No more bottles of beer on the wall.\n"
    "Time to buy more beer!"
)

BOTTLE_SINGULAR: Final[str] = "bottle"
BOTTLE_PLURAL: Final[str] = "bottles"


# ========================================================================
# Logic Functions
# ========================================================================

def get_bounded_integer(lower_bound: int, upper_bound: int) -> int:
    """
    Prompt the user for an integer within a specified range.

    Parameters
    ----------
    lower_bound : int
        The minimum accepted integer value.
    upper_bound : int
        The maximum accepted integer value.

    Returns
    -------
    int
        The validated integer entered by the user.
    """
    while True:
        user_input: str = input(BOTTLE_PROMPT).strip()

        try:
            validated_integer: int = int(user_input)
        except ValueError:
            print(INTEGER_ERROR_MESSAGE)
            continue

        if user_input != str(validated_integer):
            print(INTEGER_ERROR_MESSAGE)
            continue

        if lower_bound <= validated_integer <= upper_bound:
            return validated_integer

        print(RANGE_ERROR_MESSAGE)

    raise RuntimeError("get_bounded_integer() reached an unexpected state")


def bottle_countdown(bottles_count: int) -> None:
    """
    Count down bottles of beer from the supplied value to zero.

    Parameters
    ----------
    bottles_count : int
        The validated number of bottles to begin the countdown.

    Returns
    -------
    None
    """
    bottle_count: int = bottles_count

    while bottle_count >= 1:
        current_bottle_word: str = plurality(
            bottle_count,
            BOTTLE_SINGULAR,
            BOTTLE_PLURAL
        )

        print(
            f"{bottle_count} {current_bottle_word} of beer on the wall, "
            f"{bottle_count} {current_bottle_word} of beer."
        )
        print("Take one down and pass it around.")

        bottle_count -= 1

        remaining_bottle_word: str = plurality(
            bottle_count,
            BOTTLE_SINGULAR,
            BOTTLE_PLURAL
        )

        print(
            f"{bottle_count} {remaining_bottle_word} of beer on the wall.\n"
        )

    print(REMINDER_MESSAGE)


def plurality(
        bottles_count: int,
        singular_form: str,
        plural_form: str
) -> str:
    """
    Return the singular or plural form based on a bottle count.

    Parameters
    ----------
    bottles_count : int
        The number of bottles being described.
    singular_form : str
        The word to return when the bottle count equals one.
    plural_form : str
        The word to return for all other bottle counts.

    Returns
    -------
    str
        The singular form when bottles_count equals one; otherwise, the
        plural form.
    """
    if bottles_count == 1:
        return singular_form

    return plural_form


# ========================================================================
# Main Function
# ========================================================================

def main() -> None:
    """
    Run the bottles of beer countdown program.

    Returns
    -------
    None
    """
    print(TITLE_TEXT)
    bottles_count: int = get_bounded_integer(
        MINIMUM_BOTTLES,
        MAXIMUM_BOTTLES
    )
    bottle_countdown(bottles_count)


if __name__ == "__main__":
    main()

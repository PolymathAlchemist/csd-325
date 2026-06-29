"""
CIS245-T303 Introduction to Programming
Instructor: Professor Ed Parks
Assignment: Module 3 - Cho-Han Dice Game Refactor
Author: Eric J. Turman
Date: 2026-06-26
Email: ejturman@my365.bellevue.edu

Rebuilt from Cho-Han, by Al Sweigart al@inventwithpython.com
The traditional Japanese dice game of even-odd.
View this code athttps://nostarch.com/big-book-small-python-projects

The program plays Cho-Han, a traditional Japanese dice game. The player
starts with a purse of 5000 mon and wagers on whether two dice will total
an even number, CHO, or an odd number, HAN.

This refactored version preserves the original game behavior while improving
the structure with named constants, descriptive function names, type hints,
and reusable single-purpose functions. It also includes assignment specific
alterations.
"""

import random
import sys
from typing import Final


# ========================================================================
# Named Constants
# ========================================================================
INTRO_MESSAGE: Final[str] = """Cho-Han, by Al Sweigart al@inventwithpython.com

In this traditional Japanese dice game, two dice are rolled in a bamboo
cup by the dealer sitting on the floor. The player must guess if the
dice total to an even (cho) or odd (han) number. If the total of the dice is 
either 2 or 7, you receive a 10 mon bonus. 
"""

JAPANESE_NUMBERS: Final[dict[int, str]] = {
    1: "ICHI",
    2: "NI",
    3: "SAN",
    4: "SHI",
    5: "GO",
    6: "ROKU",
}

STARTING_PURSE: Final[int] = 5000
HOUSE_FEE_PERCENT: Final[int] = 12
BONUS_AMOUNT: Final[int] = 10
BONUS_TOTALS: Final[tuple[int, int]] = (2, 7)
INPUT_PROMPT: Final[str] = "ejt: "
QUIT_COMMAND: Final[str] = "QUIT"
CHO_BET: Final[str] = "CHO"
HAN_BET: Final[str] = "HAN"


# ========================================================================
# Input Helper Functions
# ========================================================================
def get_wager(current_purse: int) -> int:
    """
    Get a valid wager from the player.

    Parameters
    ----------
    current_purse : int
        The amount of mon currently available to the player.

    Returns
    -------
    int
        The validated wager amount.
    """
    while True:
        wager_text = input(INPUT_PROMPT)

        if wager_text.upper() == QUIT_COMMAND:
            print("Thanks for playing!")
            sys.exit()

        if not wager_text.isdecimal():
            print("Please enter a number.")
            continue

        wager = int(wager_text)
        if wager > current_purse:
            print("You do not have enough to make that bet.")
            continue

        return wager


def get_player_bet() -> str:
    """
    Get the player's CHO or HAN bet.

    Returns
    -------
    str
        The validated player bet, either CHO or HAN.
    """
    while True:
        player_bet = input(INPUT_PROMPT).upper()

        if player_bet in (CHO_BET, HAN_BET):
            return player_bet

        print('Please enter either "CHO" or "HAN".')


# ========================================================================
# Dice and Game Rule Functions
# ========================================================================
def roll_dice() -> tuple[int, int]:
    """
    Roll two six-sided dice.

    Returns
    -------
    tuple[int, int]
        The two dice values.
    """
    return random.randint(1, 6), random.randint(1, 6)


def get_correct_bet(roll_total: int) -> str:
    """
    Determine the winning bet for a dice total.

    Parameters
    ----------
    roll_total : int
        The total of the two rolled dice.

    Returns
    -------
    str
        CHO when the total is even, otherwise HAN.
    """
    if roll_total % 2 == 0:
        return CHO_BET

    return HAN_BET


def get_house_fee(wager: int) -> int:
    """
    Calculate the house fee for a winning wager.

    Parameters
    ----------
    wager : int
        The player's wager amount.

    Returns
    -------
    int
        The 12 percent house fee, rounded down to whole mon.
    """
    return (wager * HOUSE_FEE_PERCENT) // 100


def apply_bonus(current_purse: int, roll_total: int) -> int:
    """
    Apply the bonus when the dice total is eligible.

    Parameters
    ----------
    current_purse : int
        The player's current purse after the wager result.
    roll_total : int
        The total of the two rolled dice.

    Returns
    -------
    int
        The updated purse total.
    """
    if roll_total in BONUS_TOTALS:
        print(f"The dealer rolled {roll_total} You got a bonus of 10 mon!")
        return current_purse + BONUS_AMOUNT

    return current_purse


# ========================================================================
# Display Helper Functions
# ========================================================================
def display_intro() -> None:
    """
    Display the game introduction.

    Returns
    -------
    None
    """
    print(INTRO_MESSAGE)


def display_wager_prompt(current_purse: int) -> None:
    """
    Display the player's current purse and wager prompt.

    Parameters
    ----------
    current_purse : int
        The player's current purse.

    Returns
    -------
    None
    """
    print(f"You have {current_purse} mon. How much do you bet? (or QUIT)")


def display_dealer_prompt() -> None:
    """
    Display the dealer's prompt before the CHO or HAN bet.

    Returns
    -------
    None
    """
    print("The dealer swirls the cup and you hear the rattle of dice.")
    print("The dealer slams the cup on the floor, still covering the")
    print("dice and asks for your bet.")
    print()
    print("    CHO (even) or HAN (odd)?")


def display_dice_result(first_die: int, second_die: int) -> None:
    """
    Display the dice result in Japanese and numeric form.

    Parameters
    ----------
    first_die : int
        The value of the first die.
    second_die : int
        The value of the second die.

    Returns
    -------
    None
    """
    print("The dealer lifts the cup to reveal:")
    print(f"   {JAPANESE_NUMBERS[first_die]} - {JAPANESE_NUMBERS[second_die]}")
    print(f"     {first_die} - {second_die}")


def display_game_over() -> None:
    """
    Display the game-over messages.

    Returns
    -------
    None
    """
    print("You have run out of money!")
    print("Thanks for playing!")


# ========================================================================
# Round Processing Functions
# ========================================================================
def update_purse_for_result(
        current_purse: int,
        wager: int,
        player_won: bool
) -> int:
    """
    Update the player's purse based on whether the player won.

    Parameters
    ----------
    current_purse : int
        The player's purse before resolving the wager.
    wager : int
        The player's wager amount.
    player_won : bool
        True if the player guessed correctly, otherwise False.

    Returns
    -------
    int
        The updated purse after winnings, loss, and house fee.
    """
    if player_won:
        house_fee = get_house_fee(wager)
        print(f"You won! You take {wager} mon.")
        print(f"The house collects a {house_fee} mon fee.")
        return current_purse + wager - house_fee

    print("You lost!")
    return current_purse - wager


def play_round(current_purse: int) -> int:
    """
    Play one round of Cho-Han.

    Parameters
    ----------
    current_purse : int
        The player's purse at the start of the round.

    Returns
    -------
    int
        The player's purse after the completed round.
    """
    display_wager_prompt(current_purse)
    wager = get_wager(current_purse)
    first_die, second_die = roll_dice()

    display_dealer_prompt()
    player_bet = get_player_bet()

    display_dice_result(first_die, second_die)

    roll_total = first_die + second_die
    correct_bet = get_correct_bet(roll_total)
    player_won = player_bet == correct_bet

    updated_purse = update_purse_for_result(
        current_purse,
        wager,
        player_won
    )

    return apply_bonus(updated_purse, roll_total)


# ========================================================================
# Program Entry Point
# ========================================================================
def main() -> None:
    """
    Entry point for the program.

    Returns
    -------
    None
    """
    display_intro()
    purse = STARTING_PURSE

    while True:
        purse = play_round(purse)

        if purse == 0:
            display_game_over()
            sys.exit()


if __name__ == "__main__":
    main()

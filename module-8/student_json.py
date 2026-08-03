"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 8 - JSON Practice
Author: Eric J. Turman
Date: 2026-08-02
Email: ejturman@my365.bellevue.edu

Description:
------------

Read, display, update, and save student JSON data.

Notes:
------

The student data file is resolved relative to this source file so the
program does not depend on the current working directory.
"""

# ============================================================================
# Imports
# ============================================================================

import json
from pathlib import Path


# ============================================================================
# Constants
# ============================================================================

STUDENT_FILE = Path(__file__).resolve().parent / "Student.json"

NEW_STUDENT: dict[str, str | int] = {
    "F_Name": "Eric",
    "L_Name": "Turman",
    "Student_ID": 73921,
    "Email": "eric.turman@example.com",
}


# ============================================================================
# Functions
# ============================================================================

def load_students() -> list[dict[str, str | int]]:
    """Load the student records from the JSON data file.

    Returns
    -------
    list[dict[str, str | int]]
        Student records loaded from the JSON data file.
    """
    with STUDENT_FILE.open("r", encoding="utf-8") as file:
        students = json.load(file)

    return students


def display_students(students: list[dict[str, str | int]]) -> None:
    """Print each student record on one line.

    Parameters
    ----------
    students
        Student records to display.

    Returns
    -------
    None
    """
    for student in students:
        print(
            f"{student['L_Name']}, {student['F_Name']} : "
            f"ID = {student['Student_ID']} , Email = {student['Email']}"
        )


def save_students(students: list[dict[str, str | int]]) -> None:
    """Save the student records to the JSON data file.

    Parameters
    ----------
    students
        Student records to save.

    Returns
    -------
    None
    """
    with STUDENT_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


# ============================================================================
# Main Program Flow
# ============================================================================

def main() -> None:
    """Display, update, and save the student records.

    Returns
    -------
    None
    """
    students = load_students()

    print("Original Student List")
    display_students(students)

    students.append(NEW_STUDENT.copy())

    print("\nUpdated Student List")
    display_students(students)

    save_students(students)

    print("\nThe student file was updated.")


# ============================================================================
# Program Entry Point
# ============================================================================

if __name__ == "__main__":
    main()

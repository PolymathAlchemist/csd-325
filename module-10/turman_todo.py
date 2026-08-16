"""
Course: CSD325 Advanced Python
Instructor: Parks
Assignment: Module 10 - GUI ToDo
Author: Eric J. Turman
Date: 2026-08-13
Email: ejturman@my365.bellevue.edu

Original attribution:
---------
This program is adapted from Listing 2.2, "Our Scrolling To-Do,"
in David Love's Python Tkinter By Example (2018). The implementation
has been substantially refactored and modified to meet the
Module 10 assignment requirements.

Description:
------------

Create a scrolling graphical ToDo list with task entry, complementary task
colors, confirmed right-click deletion, and a File menu.

Notes:
------

Tasks are added by pressing Enter and can only be deleted by right-clicking
the task and confirming the deletion.
"""

# ============================================================================
# Imports
# ============================================================================

from typing import ClassVar

import tkinter as tk
from tkinter import messagebox


# ============================================================================
# Class Definitions
# ============================================================================

class Todo(tk.Tk):
    """
    Represent the scrolling graphical ToDo application.

    Notes
    -----
    The application uses one Tk root window and one main event loop.
    """

    BELLEVUE_PURPLE: ClassVar[str] = "#5C3B8E"
    BELLEVUE_GOLD: ClassVar[str] = "#F2C318"
    TASK_COLOR_SCHEMES: ClassVar[tuple[dict[str, str], dict[str, str]]] = (
        {"bg": BELLEVUE_GOLD, "fg": "black"},
        {"bg": BELLEVUE_PURPLE, "fg": "white"},
    )

    # ========================================================================
    # Initialization
    # ========================================================================

    def __init__(self) -> None:
        """
        Initialize the root window and its graphical components.
        """
        super().__init__()
        self.title("Turman-ToDo")
        self.geometry("600x480")
        self.minsize(420, 320)
        self._build_menu()

        tk.Label(
            self,
            text="Right-click a task to delete it.",
            bg=self.BELLEVUE_PURPLE, fg="white",
            font=("Segoe UI", 11, "bold"), padx=12, pady=10,
        ).pack(fill="x")

        list_frame: tk.Frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True)
        self.canvas: tk.Canvas = tk.Canvas(
            list_frame,
            bg="white",
            highlightthickness=0
        )
        scrollbar: tk.Scrollbar = tk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.task_frame: tk.Frame = tk.Frame(self.canvas, bg="white")
        self.task_window: int = self.canvas.create_window(
            (0, 0),
            window=self.task_frame,
            anchor="nw"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        entry_frame: tk.Frame = tk.Frame(
            self,
            bg=self.BELLEVUE_PURPLE,
            padx=10,
            pady=10
        )
        entry_frame.pack(side="bottom", fill="x")
        tk.Label(
            entry_frame,
            text="New task (press Enter):",
            bg=self.BELLEVUE_PURPLE,
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")
        self.task_entry: tk.Text = tk.Text(
            entry_frame,
            height=2,
            wrap="word"
        )
        self.task_entry.pack(fill="x", pady=(4, 0))
        self.task_entry.bind("<Return>", self.add_task)
        self.task_entry.focus_set()

        self.task_frame.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_task_width)
        self.canvas.bind_all("<MouseWheel>", self._scroll_tasks)
        self.canvas.bind_all("<Button-4>", self._scroll_tasks)
        self.canvas.bind_all("<Button-5>", self._scroll_tasks)

    # ========================================================================
    # Menu Configuration
    # ========================================================================

    def _build_menu(self) -> None:
        """
        Create and attach the File menu to the root window.
        """
        menu_bar: tk.Menu = tk.Menu(self)
        file_menu: tk.Menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.configure(menu=menu_bar)

    # ========================================================================
    # Task Management
    # ========================================================================

    def add_task(self, _event: tk.Event | None = None) -> str:
        """
        Add nonempty entry text to the task list.

        Parameters
        ----------
        _event : tkinter.Event or None, optional
            Return-key event that requested the task addition.

        Returns
        -------
        str
            The Tkinter callback value that prevents a newline insertion.
        """
        task_text: str = self.task_entry.get("1.0", "end").strip()
        if task_text:
            task: tk.Label = tk.Label(
                self.task_frame,
                text=task_text,
                anchor="w",
                justify="left",
                padx=14,
                pady=11,
                font=("Segoe UI", 11),
            )
            task.pack(fill="x")
            task.bind("<Button-3>", self.delete_task)
            self.task_entry.delete("1.0", "end")
            self._recolor_tasks()
        return "break"

    def delete_task(self, event: tk.Event) -> None:
        """
        Request confirmation before deleting the selected task.

        Parameters
        ----------
        event : tkinter.Event
            Right-click event whose widget identifies the selected task.
        """
        task: tk.Misc = event.widget
        if not isinstance(task, tk.Label):
            return

        if messagebox.askyesno(
                "Delete task",
                f"Delete '{task.cget('text')}'?",
                parent=self
        ):
            task.destroy()
            self.after_idle(self._recolor_tasks)

    def _recolor_tasks(self) -> None:
        """
        Restore alternating task colors after a list change.
        """
        tasks: list[tk.Misc] = self.task_frame.winfo_children()

        for index, task in enumerate(tasks):
            color_scheme: dict[str, str] = self.TASK_COLOR_SCHEMES[index % 2]
            task.configure(**color_scheme)

    # ========================================================================
    # Canvas Event Handling
    # ========================================================================

    def _update_scrollregion(self, _event: tk.Event) -> None:
        """
        Update the canvas scroll region after task-frame resizing.

        Parameters
        ----------
        _event : tkinter.Event
            Configure event generated by the task frame.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_task_width(self, event: tk.Event) -> None:
        """
        Match the embedded task frame to the canvas width.

        Parameters
        ----------
        event : tkinter.Event
            Canvas configure event containing the current width.
        """
        self.canvas.itemconfigure(self.task_window, width=event.width)

    def _scroll_tasks(self, event: tk.Event) -> None:
        """
        Scroll the task canvas in response to mouse-wheel input.

        Parameters
        ----------
        event : tkinter.Event
            Platform-specific mouse-wheel event and scroll direction.
        """
        direction: int = -1 if getattr(
            event,
            "num",
            None) == 4 or getattr(
            event,
            "delta",
            0) > 0 else 1
        self.canvas.yview_scroll(direction, "units")

# ============================================================================
# Main program flow
# ============================================================================

def main() -> None:
    """
    Create and run the ToDo application.
    """
    todo: Todo = Todo()
    todo.mainloop()

# ============================================================================
# Program Entry Point
# ============================================================================

if __name__ == "__main__":
    main()

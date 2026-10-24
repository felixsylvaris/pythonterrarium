
"""
Quick Notes
A terminal program for saving notes in a JSON file.
Supports adding, displaying, deleting, searching, and opening notes.
"""

import json
import os
from datetime import datetime, timezone


# ---------- FILE FUNCTIONS ----------

def load_notes(file_path):
    """Load notes from JSON, or return an empty list."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notes(file_path, notes):
    """Save notes to JSON."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4)


# ---------- NOTE FUNCTIONS ----------

def display_notes(notes, full_list=False):
    """Display the newest 10 notes or all notes."""
    selected = notes if full_list else notes[-10:]

    if not selected:
        print("No notes available.")
        return

    for number, note in enumerate(reversed(selected), 1):
        print(f"{number}. {note['title']} - {note['created_at']}")
        print(f"   {note['content']}\n")


def add_note(notes):
    """Create a new note."""
    title = input("Title: ")
    content = input("Content: ")

    notes.append({
        "title": title,
        "content": content,
        "created_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    })

    print("Note added.")


def delete_note(notes):
    """Delete a note by its number in the full newest-first list."""
    if not notes:
        print("No notes available.")
        return

    display_notes(notes, full_list=True)

    try:
        number = int(input("Number to delete: "))
        if not 1 <= number <= len(notes):
            raise ValueError
    except ValueError:
        print("Invalid note number.")
        return

    del notes[-number]
    print("Note deleted.")


def open_note(note):
    """Display one complete note."""
    print(f"\n{note['title']}")
    print(f"Created: {note['created_at']}")
    print(f"Content: {note['content']}\n")


def search_notes(notes):
    """Search titles and contents."""
    query = input("Search: ").lower()

    results = [
        note for note in notes
        if query in note["title"].lower()
        or query in note["content"].lower()
    ]

    display_notes(results, full_list=True)


def open_by_number(notes):
    """Open a note from the latest 10."""
    display_notes(notes)

    if not notes:
        return

    try:
        number = int(input("Number to open: "))
        if not 1 <= number <= min(10, len(notes)):
            raise ValueError
    except ValueError:
        print("Invalid note number.")
        return

    open_note(notes[-number])


def open_by_title(notes):
    """Open the newest note with the matching title."""
    title = input("Title to open: ").lower()

    for note in reversed(notes):
        if note["title"].lower() == title:
            open_note(note)
            return

    print("Note not found.")


# ---------- MAIN MENU ----------

def main():
    file_path = os.path.join(os.path.dirname(__file__), "notes.json")
    notes = load_notes(file_path)

    actions = {
        "1": lambda: display_notes(notes),
        "2": lambda: display_notes(notes, full_list=True),
        "3": lambda: add_note(notes),
        "4": lambda: delete_note(notes),
        "5": lambda: search_notes(notes),
        "6": lambda: open_by_number(notes),
        "7": lambda: open_by_title(notes),
    }

    while True:
        print("""
Quick Notes
1. Display latest 10 notes
2. Display all notes
3. Add note
4. Delete note
5. Search notes
6. Open note by number
7. Open note by title
8. Exit
""")

        choice = input("Choice: ")

        if choice == "8":
            print("Goodbye!")
            break

        if choice in actions:
            old_notes = notes.copy()
            actions[choice]()

            if notes != old_notes:
                save_notes(file_path, notes)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

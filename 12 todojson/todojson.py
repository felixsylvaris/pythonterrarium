
import json
from datetime import date, timedelta


# ---------- TASK FUNCTIONS ----------

def add_task(todo_list, task_date, task):
    if task_date not in todo_list:
        todo_list[task_date] = []

    todo_list[task_date].append({
        "task": task,
        "status": "TODO"
    })


def remove_task(todo_list, task_date, task_number):
    todo_list[task_date].pop(task_number - 1)

    # Remove the date if no tasks remain.
    if not todo_list[task_date]:
        del todo_list[task_date]


def mark_task_done(todo_list, task_date, task_number):
    todo_list[task_date][task_number - 1]["status"] = "DONE"


# ---------- DISPLAY FUNCTIONS ----------

def print_available_dates(todo_list):
    if not todo_list:
        print("No tasks available.")
        return

    print("\nAvailable dates:")
    for task_date in sorted(todo_list):
        print(task_date)


def print_tasks(todo_list, task_date):
    if task_date not in todo_list:
        print("No tasks for this date.")
        return False

    print(f"\nTasks for {task_date}:")

    for number, task in enumerate(todo_list[task_date], start=1):
        print(f"{number}. [{task['status']}] {task['task']}")

    return True


# ---------- INPUT FUNCTIONS ----------

def choose_date():
    today = date.today()

    print("\nChoose a date:")
    print("Press Enter for today.")
    print("You can also enter today, tomorrow, yesterday,")
    print("or a date in YYYY-MM-DD format.")

    choice = input("Date: ").strip().lower()

    if choice == "" or choice == "today":
        selected_date = today
    elif choice == "tomorrow":
        selected_date = today + timedelta(days=1)
    elif choice == "yesterday":
        selected_date = today - timedelta(days=1)
    else:
        try:
            selected_date = date.fromisoformat(choice)
        except ValueError:
            print("Invalid date.")
            return None

    return selected_date.isoformat()


def choose_task_number(todo_list, task_date):
    if not print_tasks(todo_list, task_date):
        return None

    try:
        number = int(input("Enter task number: "))

        if 1 <= number <= len(todo_list[task_date]):
            return number

        print("Invalid task number.")
        return None

    except ValueError:
        print("Please enter a number.")
        return None


# ---------- FILE FUNCTIONS ----------

def save_to_file(todo_list, filename):
    with open(filename, "w") as file:
        json.dump(todo_list, file, indent=4)


def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# ---------- MAIN PROGRAM ----------

def main():
    filename = "todo_list.json"
    todo_list = load_from_file(filename)

    while True:
        print("\n=== TODO LIST ===")
        print("1. Add task")
        print("2. Remove task")
        print("3. Mark task as DONE")
        print("4. View tasks")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            task_date = choose_date()

            if task_date is None:
                continue

            task = input("Enter task: ").strip()

            if task:
                add_task(todo_list, task_date, task)
                save_to_file(todo_list, filename)
                print("Task added.")
            else:
                print("Task cannot be empty.")

        elif choice == "2":
            task_date = choose_date()

            if task_date is None:
                continue

            number = choose_task_number(todo_list, task_date)

            if number is not None:
                remove_task(todo_list, task_date, number)
                save_to_file(todo_list, filename)
                print("Task removed.")

        elif choice == "3":
            task_date = choose_date()

            if task_date is None:
                continue

            number = choose_task_number(todo_list, task_date)

            if number is not None:
                mark_task_done(todo_list, task_date, number)
                save_to_file(todo_list, filename)
                print("Task marked as DONE.")

        elif choice == "4":
            print_available_dates(todo_list)

            task_date = choose_date()

            if task_date is not None:
                print_tasks(todo_list, task_date)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

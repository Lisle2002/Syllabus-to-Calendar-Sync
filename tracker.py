import json
import os
from datetime import datetime

FILE_NAME = 'deadlines.json'

def load_deadlines():
    """Loads existing deadlines, fixing broken or completely empty files automatically."""
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        return []
    
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If the file is broken or lacks the [] brackets, return an empty list safely
        return []

def save_deadlines(deadlines):
    """Saves deadlines to the JSON file."""
    with open(FILE_NAME, 'w') as file:
        json.dump(deadlines, file, indent=4)

def add_deadline(deadlines):
    """Prompts the user to add a new task."""
    course = input("Course Name (e.g., CS101): ")
    task = input("Task (e.g., Midterm Essay): ")
    description = input("Description/Notes (optional): ")
    
    while True:
        date_str = input("Due Date (YYYY-MM-DD): ")
        try:
            valid_date = datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            
    while True:
        time_str = input("Due Time (e.g., 11:59 PM, press Enter for 11:59 PM): ").strip().upper()
        if not time_str:
            time_str = "11:59 PM"
            break
        try:
            datetime.strptime(time_str, "%I:%M %p")
            break
        except ValueError:
            print("Invalid time format! Please use HH:MM AM/PM (e.g., 08:00 PM).")

    new_task = {
        "course": course,
        "task": task,
        "due_date": date_str,
        "due_time": time_str
    }
    
    if description:
        new_task["description"] = description

    deadlines.append(new_task)
    save_deadlines(deadlines)
    print(f"\nSuccess! Added '{task}' for {course} at {time_str}.")

def view_deadlines(deadlines):
    """Displays all deadlines sorted by date."""
    if not deadlines:
        print("\nNo deadlines found! You're all caught up.")
        return

    sorted_deadlines = sorted(deadlines, key=lambda x: datetime.strptime(x["due_date"], "%Y-%m-%d"))
    
    print("\n--- Upcoming Deadlines ---")
    for item in sorted_deadlines:
        due = datetime.strptime(item["due_date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        days_left = (due - today).days

        time_display = item.get("due_time", "11:59 PM")
        urgency = f"({days_left} days left)" if days_left >= 0 else "(OVERDUE!)"
        print(f"[{item['due_date']} {time_display}] {item['course']} - {item['task']} {urgency}")
    print("--------------------------\n")

def main():
    deadlines = load_deadlines()
    
    while True:
        print("\nSyllabus Deadline Tracker")
        print("1. View upcoming deadlines")
        print("2. Add a new deadline")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            view_deadlines(deadlines)
        elif choice == '2':
            add_deadline(deadlines)
        elif choice == '3':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()

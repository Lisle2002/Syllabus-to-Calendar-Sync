import json
import os
from datetime import datetime

FILE_NAME = 'deadlines.json'

def load_deadlines():
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        return []
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_deadlines(deadlines):
    with open(FILE_NAME, 'w') as file:
        json.dump(deadlines, file, indent=4)

def add_deadline(deadlines):
    print("\n--- Add New Task ---")
    
    # --- TWEAK 1: Prevent Blank Inputs ---
    while True:
        course = input("Project/Category Name: ").strip()
        if course: break
        print("Error: Project name cannot be blank.")
        
    while True:
        task = input("Task/Milestone: ").strip()
        if task: break
        print("Error: Task name cannot be blank.")
        
    description = input("Description/Notes (optional): ").strip()
    
    while True:
        date_str = input("Due Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            
    while True:
        time_str = input("Due Time (e.g., 08:00 PM, press Enter for 11:59 PM): ").strip().upper()
        if not time_str:
            time_str = "11:59 PM"
            break
        try:
            datetime.strptime(time_str, "%I:%M %p")
            break
        except ValueError:
            print("Invalid time format! Please use HH:MM AM/PM.")

    tz_str = input("Timezone (e.g., EST, CST, PST. Press Enter for Local Time): ").strip().upper()

    while True:
        rem_str = input("Remind me how many minutes before? (press Enter for 30): ").strip()
        if not rem_str:
            rem_str = "30"
            break
        if rem_str.isdigit():
            break
        print("Please enter a valid number of minutes.")

    new_task = {
        "course": course,
        "task": task,
        "due_date": date_str,
        "due_time": time_str,
        "timezone": tz_str,
        "reminder": rem_str
    }
    
    if description:
        new_task["description"] = description

    deadlines.append(new_task)
    save_deadlines(deadlines)
    print(f"\nSuccess! Added '{task}' for {course} at {time_str} {tz_str}.")

def view_deadlines(deadlines):
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
        tz_display = f" {item.get('timezone', '')}".rstrip()
        rem_display = f" [⏰ {item.get('reminder', '30')}m]"

        urgency = f"({days_left} days left)" if days_left >= 0 else "(OVERDUE!)"
        print(f"[{item['due_date']} {time_display}{tz_display}]{rem_display} {item['course']} - {item['task']} {urgency}")
    print("--------------------------\n")

def main():
    deadlines = load_deadlines()
    
    while True:
        print("\nProject & Deadline Tracker")
        print("1. View upcoming deadlines")
        print("2. Add a new deadline")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            view_deadlines(deadlines)
        elif choice == '2':
            add_deadline(deadlines)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

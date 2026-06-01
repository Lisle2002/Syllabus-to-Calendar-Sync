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
        date_str = input("Start Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            
    while True:
        start_str = input("Start Time (e.g., 01:00 PM, press Enter for 11:59 PM): ").strip().upper()
        if not start_str:
            start_str = "11:59 PM"
            break
        try:
            datetime.strptime(start_str, "%I:%M %p")
            break
        except ValueError:
            print("Invalid time format! Please use HH:MM AM/PM.")

    while True:
        end_str = input("End Time (e.g., 03:00 PM, press Enter for 1 hour duration): ").strip().upper()
        if not end_str:
            end_str = ""
            break
        try:
            datetime.strptime(end_str, "%I:%M %p")
            break
        except ValueError:
            print("Invalid time format! Please use HH:MM AM/PM.")

    tz_str = input("Timezone (e.g., EST, EDT, CST. Press Enter for Local Time): ").strip().upper()

    while True:
        rem_str = input("Remind me how many minutes before? (press Enter for 30): ").strip()
        if not rem_str:
            rem_str = "30"
            break
        if rem_str.isdigit():
            break
        print("Please enter a valid number of minutes.")

    while True:
        repeat_str = input("Repeat Weekly? (Enter number of weeks, e.g., 15, or press Enter for No): ").strip()
        if not repeat_str:
            repeat_str = "0"
            break
        if repeat_str.isdigit():
            break
        print("Please enter a valid number.")

    new_task = {
        "course": course,
        "task": task,
        "due_date": date_str,
        "due_time": start_str,
        "end_time": end_str,
        "timezone": tz_str,
        "reminder": rem_str,
        "repeat_weeks": repeat_str
    }
    
    if description:
        new_task["description"] = description

    deadlines.append(new_task)
    save_deadlines(deadlines)
    print(f"\nSuccess! Added '{task}' for {course}.")

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

        start_display = item.get("due_time", "11:59 PM")
        end_display = item.get("end_time", "")
        time_display = f"{start_display} - {end_display}" if end_display else start_display
        
        tz_display = f" {item.get('timezone', '')}".rstrip()
        rem_display = f" [⏰ {item.get('reminder', '30')}m]"
        rep_display = f" [🔁 {item.get('repeat_weeks')} weeks]" if int(item.get('repeat_weeks', '0')) > 1 else ""

        urgency = f"({days_left} days left)" if days_left >= 0 else "(OVERDUE!)"
        print(f"[{item['due_date']} | {time_display}{tz_display}]{rem_display}{rep_display} {item['course']} - {item['task']} {urgency}")
    print("--------------------------\n")

# --- NEW: Delete / Complete Feature ---
def delete_deadline(deadlines):
    if not deadlines:
        print("\nNo deadlines found to delete!")
        return

    # Sort them by date so they match the visual layout in 'View'
    sorted_deadlines = sorted(deadlines, key=lambda x: datetime.strptime(x["due_date"], "%Y-%m-%d"))

    print("\n--- Delete / Complete a Task ---")
    for idx, item in enumerate(sorted_deadlines, 1):
        start_display = item.get("due_time", "11:59 PM")
        end_display = item.get("end_time", "")
        time_display = f"{start_display} - {end_display}" if end_display else start_display
        print(f"{idx}. [{item['due_date']} | {time_display}] {item['course']} - {item['task']}")
    
    cancel_option = len(sorted_deadlines) + 1
    print(f"{cancel_option}. Cancel (Go back to menu)")

    while True:
        choice = input(f"\nEnter the number of the task to remove (1-{cancel_option}): ").strip()
        if not choice:
            continue
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(sorted_deadlines):
                removed_item = sorted_deadlines[choice_num - 1]
                
                # Remove it from the original unsorted array to maintain file integrity
                deadlines.remove(removed_item)
                save_deadlines(deadlines)
                
                print(f"\nSuccess! '{removed_item['task']}' has been permanently removed.")
                break
            elif choice_num == cancel_option:
                print("\nAction canceled. Returning to main menu.")
                break
        print(f"Invalid selection. Please enter a number between 1 and {cancel_option}.")

def main():
    deadlines = load_deadlines()
    
    while True:
        print("\nProject & Deadline Tracker")
        print("1. View upcoming deadlines")
        print("2. Add a new deadline")
        print("3. Delete/Complete a deadline") # Integrated choice
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            view_deadlines(deadlines)
        elif choice == '2':
            add_deadline(deadlines)
        elif choice == '3':
            delete_deadline(deadlines)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

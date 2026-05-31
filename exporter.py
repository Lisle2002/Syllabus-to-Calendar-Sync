import json
import os
from ics import Calendar, Event
from datetime import datetime

# File paths
JSON_FILE = 'deadlines.json'
ICS_FILE = 'deadlines.ics'

def load_json_data():
    """Reads the JSON database, surviving completely empty or broken files."""
    if not os.path.exists(JSON_FILE) or os.stat(JSON_FILE).st_size == 0:
        print(f"Notice: {JSON_FILE} is missing or empty. Run your tracker first!")
        return []
    
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {JSON_FILE} contains invalid data. Please ensure it is formatted correctly.")
        return []

def generate_ics(deadlines):
    """Converts JSON data into an iCalendar file safely."""
    if not deadlines:
        print("No valid deadlines to export.")
        return

    cal = Calendar()
    valid_count = 0

    for item in deadlines:
        if not item.get('due_date') or item['due_date'].strip() == "":
            continue

        e = Event()
        e.name = f"{item.get('course', 'Unknown')} - {item.get('task', 'Task')}"
        
        date_str = item['due_date']
        time_str = item.get('due_time', '11:59 PM')
        
        try:
            parsed_time = datetime.strptime(time_str, "%I:%M %p")
            formatted_time = parsed_time.strftime("%H:%M:00")
        except ValueError:
            try:
                parsed_time = datetime.strptime(time_str, "%H:%M")
                formatted_time = parsed_time.strftime("%H:%M:00")
            except ValueError:
                formatted_time = "23:59:00"
        
        e.begin = f"{date_str} {formatted_time}"
        
        if 'description' in item:
            e.description = item['description']
        
        cal.events.add(e)
        valid_count += 1

    if valid_count > 0:
        try:
            # Safely attempt to write the file, catching permission errors
            with open(ICS_FILE, 'w') as my_file:
                my_file.writelines(cal.serialize())
            print(f"Success! Exported {valid_count} deadlines to {ICS_FILE}.")
        except PermissionError:
            print(f"\nCRITICAL ERROR: Could not save '{ICS_FILE}'.")
            print("The file is currently open in another program (like a calendar app).")
            print("Please close it and run this script again.\n")
    else:
        print("No valid deadlines with dates were found to export.")

def main():
    print("Starting conversion...")
    data = load_json_data()
    generate_ics(data)

if __name__ == "__main__":
    main()

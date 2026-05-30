import json
import os
from ics import Calendar, Event
from datetime import datetime

# File paths
JSON_FILE = 'deadlines.json'
ICS_FILE = 'deadlines.ics'

def load_json_data():
    """Reads the JSON database."""
    if not os.path.exists(JSON_FILE):
        print(f"Error: Could not find {JSON_FILE}. Run your tracker first!")
        return []
    
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def generate_ics(deadlines):
    """Converts JSON data into an iCalendar file."""
    if not deadlines:
        print("No deadlines to export.")
        return

    # Initialize a new Calendar
    cal = Calendar()

    for item in deadlines:
        # Create a new Event for each deadline
        e = Event()
        
        # Format the title (e.g., "CS101 - Midterm Essay")
        e.name = f"{item['course']} - {item['task']}"
        
        # Set the date. By passing just the date string, it becomes an all-day event.
        e.begin = item['due_date']
        
        # Add the description if it exists
        if 'description' in item:
            e.description = item['description']
        
        # Add the event to the calendar
        cal.events.add(e)

    # Save the calendar data to a .ics file
    with open(ICS_FILE, 'w') as my_file:
        my_file.writelines(cal.serialize())
    
    print(f"Success! Exported {len(deadlines)} deadlines to {ICS_FILE}.")

def main():
    print("Starting conversion...")
    data = load_json_data()
    generate_ics(data)

if __name__ == "__main__":
    main()

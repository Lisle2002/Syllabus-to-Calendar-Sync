import json
import os
import warnings
from ics import Calendar, Event
from datetime import datetime, timedelta

# --- TWEAK 3: Mute harmless library warnings ---
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ics.alarm import DisplayAlarm
except ImportError:
    try:
        from ics import DisplayAlarm
    except ImportError:
        DisplayAlarm = None

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

JSON_FILE = 'deadlines.json'
ICS_FILE = 'deadlines.ics'

TZ_MAP = {
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
}

def load_json_data():
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
        tz_input = item.get('timezone', '').strip().upper()
        
        try:
            parsed_time = datetime.strptime(time_str, "%I:%M %p")
            formatted_time = parsed_time.strftime("%H:%M:00")
        except ValueError:
            try:
                parsed_time = datetime.strptime(time_str, "%H:%M")
                formatted_time = parsed_time.strftime("%H:%M:00")
            except ValueError:
                formatted_time = "23:59:00"
        
        date_time_string = f"{date_str} {formatted_time}"
        dt = datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S")
        
        if tz_input:
            if tz_input in TZ_MAP and ZoneInfo:
                dt = dt.replace(tzinfo=ZoneInfo(TZ_MAP[tz_input]))
            else:
                print(f"Warning: Timezone '{tz_input}' not recognized. Defaulting to local time for '{e.name}'.")
            
        e.begin = dt
        
        if 'description' in item:
            e.description = item['description']
            
        if DisplayAlarm:
            try:
                reminder_mins = int(item.get('reminder', 30))
                if reminder_mins > 0:
                    alarm = DisplayAlarm(trigger=timedelta(minutes=-reminder_mins))
                    e.alarms.append(alarm)
            except ValueError:
                pass
        
        cal.events.add(e)
        valid_count += 1

    if valid_count > 0:
        try:
            with open(ICS_FILE, 'w') as my_file:
                my_file.writelines(cal.serialize())
            print(f"Success! Exported {valid_count} deadlines to {ICS_FILE}.")
        except PermissionError:
            print(f"\nCRITICAL ERROR: Could not save '{ICS_FILE}'.")
            print("The file is currently open in another program.")
            print("Please close it and run this script again.\n")
    else:
        print("No valid deadlines with dates were found to export.")

def main():
    print("Starting conversion...")
    data = load_json_data()
    generate_ics(data)

if __name__ == "__main__":
    main()

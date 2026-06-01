import json
import os
import warnings
from ics import Calendar, Event
from datetime import datetime, timedelta

warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ics.alarm import DisplayAlarm
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

        # Setup base times and strings
        date_str = item['due_date']
        start_time_str = item.get('due_time', '11:59 PM')
        end_time_str = item.get('end_time', '')
        tz_input = item.get('timezone', '').strip().upper()
        
        try:
            parsed_start = datetime.strptime(start_time_str, "%I:%M %p")
        except ValueError:
            parsed_start = datetime.strptime("11:59 PM", "%I:%M %p")
            
        if end_time_str:
            try:
                parsed_end = datetime.strptime(end_time_str, "%I:%M %p")
            except ValueError:
                parsed_end = parsed_start + timedelta(hours=1)
        else:
            parsed_end = parsed_start + timedelta(hours=1)
            
        formatted_start = parsed_start.strftime("%H:%M:00")
        formatted_end = parsed_end.strftime("%H:%M:00")
        
        base_dt_start = datetime.strptime(f"{date_str} {formatted_start}", "%Y-%m-%d %H:%M:%S")
        base_dt_end = datetime.strptime(f"{date_str} {formatted_end}", "%Y-%m-%d %H:%M:%S")
        
        if base_dt_end <= base_dt_start:
            base_dt_end += timedelta(days=1)

        # Calculate how many times to run the loop
        repeat_weeks = item.get('repeat_weeks', '0')
        loops = 1
        if str(repeat_weeks).isdigit() and int(repeat_weeks) > 0:
            loops = int(repeat_weeks)

        # --- THE NUCLEAR FAILSAFE: Loop Unrolling ---
        # Instead of writing 1 rule, we literally generate 'N' separate events
        for i in range(loops):
            e = Event()
            e.name = f"{item.get('course', 'Unknown')} - {item.get('task', 'Task')}"
            
            # Add exactly 7 days for every iteration of the loop
            current_start = base_dt_start + timedelta(weeks=i)
            current_end = base_dt_end + timedelta(weeks=i)
            
            if tz_input:
                if tz_input in TZ_MAP and ZoneInfo:
                    current_start = current_start.replace(tzinfo=ZoneInfo(TZ_MAP[tz_input]))
                    current_end = current_end.replace(tzinfo=ZoneInfo(TZ_MAP[tz_input]))
                else:
                    if i == 0: # Only print the warning on the first loop
                        print(f"Warning: Timezone '{tz_input}' not recognized. Defaulting to local time for '{e.name}'.")
                
            e.begin = current_start
            e.end = current_end
            
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
            print(f"Success! Exported {valid_count} total calendar blocks to {ICS_FILE}.")
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

# Syllabus-to-Calendar-Sync
(PROTOTYPE) A Python-based JSON to iCalendar (ICS) data converter for academic deadline automation.

(Currently Works on most Calander Applications: MUST HAVE IMPORT FUNCTION FOR THIS MODEL)

# Project & Deadline Tracker (ICS Calendar Sync)

A lightweight, bulletproof Python tool that manages your project milestones and converts them into a universal `.ics` calendar file. 

Instead of manually typing out dozens of repeating calendar events, you can use this command-line tracker to quickly generate your schedule, complete with timezones, custom reminders, and weekly repeating rules, and import it directly into Google Calendar, Outlook, or Apple Calendar.

## ✨ Features
* **Interactive CLI Menu:** Easily add, view, and delete upcoming tasks.
* **Nuclear Failsafe Recurrence:** Automatically generates perfect repeating weekly calendar blocks without relying on external calendar app logic.
* **Timezone Support:** Type in standard timezones (EST, PST, etc.) or default directly to your local computer's clock.
* **Smart Durations:** Set specific end times or let the script auto-format your event to a standard 1-hour block.
* **Custom Reminders:** Automatically injects push-notification reminders (e.g., "Remind me 30 minutes before") directly into the calendar file.

---

## 🚀 Installation & Setup

Before running the tracker, you need to install the required Python calendar library. Follow the instructions for your operating system below.

### 🪟 Windows Instructions
1. Download and extract this repository to your computer (e.g., your Desktop).
2. Open **PowerShell** or **Command Prompt**.
3. Navigate to the folder:
   ```cmd
   cd Desktop\Syllabus-to-Calendar-Sync-main
4. Install the required calendar library:
     DOS
     pip install -r requirements.txt
----------------
🍎 Mac / macOS Instructions
1.     Download and extract this repository to your computer (e.g., your Desktop).
2.    Open the Terminal app.
3.    Navigate to the folder:
cd Desktop/Syllabus-to-Calendar-Sync-main
4.    Install the required calendar library (Macs use pip3):
pip3 install -r requirements.txt


🛠️ How to Use
Once your setup is complete, you will use two scripts to manage your schedule.

1. Manage Your Tasks (tracker.py)
Run the tracker to open the interactive main menu. Here you can add new tasks, view your upcoming schedule, or delete tasks you have finished or entered incorrectly.

Windows: python tracker.py
Mac: python3 tracker.py
Note: All of your tasks are safely stored in a local deadlines.json database. Do not delete this file!

2. Export to Calendar (exporter.py)
When you are done adding or modifying tasks, run the exporter. This script reads your database and cleanly builds the deadlines.ics file.

Windows: python exporter.py
Mac: python3 exporter.py
3. Import
1.   Open Google Calendar (or your preferred calendar app).
2.   Go to Settings > Import & Export.
3.   Upload the generated deadlines.ics file.
4.   Your events, repeating weeks, and reminders will instantly populate on your calendar grid!

(NOTE)
Make Sure to have Python.
If you are unable to run the commands after opening the files / Unzipping. Open the ZipFile & Drag the File out and place it on the desktop.

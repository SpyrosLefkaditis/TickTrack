# TickTrack - SOC Ticketing System

**TickTrack** is a lightweight, user-friendly SOC (Security Operations Center) ticketing system built with Python and PyQt5. It allows SOC analysts to manage and track tickets efficiently, ensuring critical signals are handled with the appropriate severity level. 

## Features

- **Create Tickets**: Quickly create new tickets with details like signal name, description, and severity (1, 2, or 3).
- **Persistent Storage**: Tickets are saved locally in a JSON file, so they remain available even after restarting the app.
- **Dashboard**: View the count of tickets grouped by severity level in real-time.
- **Interactive Table**: Manage tickets with an intuitive table interface displaying key ticket details.
- **Modern UI**: Powered by PyQt5 for a responsive and visually appealing interface.

## How to Use

1. **Install Dependencies**:
   Install PyQt5:
   ```bash
   pip install pyqt5
2. **Download TickTrack**
    Clone The Repository:
   ```bash
   git clone  https://github.com/SpyrosLefkaditis/TickTrack.git
   
3. **Navigate to the Project Directory:**
   ```bash
   cd TickTrack
4.**Run the Application**
```bash
python TickTrack.py

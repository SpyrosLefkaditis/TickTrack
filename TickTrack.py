import sys
import uuid
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget
)

TICKET_FILE = "tickets.json"


class TickTrackApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TickTrack - SOC Ticketing System")
        self.setGeometry(100, 100, 1000, 600)

        # Load tickets from storage
        self.tickets = self.load_tickets()

        # Main layout
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Tabs
        self.main_tab = QWidget()
        self.dashboard_tab = QWidget()

        self.tabs.addTab(self.main_tab, "Create Ticket")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.init_main_tab()
        self.init_dashboard_tab()
        self.populate_ticket_table()

    def init_main_tab(self):
        """Initializes the Create Ticket tab."""
        layout = QVBoxLayout()

        # Input fields
        self.signal_input = QLineEdit(self)
        self.signal_input.setPlaceholderText("Enter Signal Name")

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter Ticket Description")

        self.severity_input = QLineEdit(self)
        self.severity_input.setPlaceholderText("Enter Severity Level (1, 2, or 3)")

        # Buttons
        self.create_ticket_button = QPushButton("Create Ticket", self)
        self.create_ticket_button.clicked.connect(self.create_ticket)

        # Ticket Table
        self.ticket_table = QTableWidget(self)
        self.ticket_table.setColumnCount(5)
        self.ticket_table.setHorizontalHeaderLabels(["Ticket ID", "Timestamp", "Signal", "Severity", "Status"])
        self.ticket_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Adding widgets to layout
        layout.addWidget(QLabel("Signal Name:"))
        layout.addWidget(self.signal_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Severity Level:"))
        layout.addWidget(self.severity_input)
        layout.addWidget(self.create_ticket_button)
        layout.addWidget(self.ticket_table)

        self.main_tab.setLayout(layout)

    def init_dashboard_tab(self):
        """Initializes the Dashboard tab."""
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("<h1>Ticket Dashboard</h1>"))

        # Severity Widgets
        self.severity_labels = {
            1: QLabel("Severity 1: No tickets yet.", self),
            2: QLabel("Severity 2: No tickets yet.", self),
            3: QLabel("Severity 3: No tickets yet.", self),
        }
        for severity, label in self.severity_labels.items():
            layout.addWidget(label)

        self.dashboard_tab.setLayout(layout)
        self.update_dashboard()

    def create_ticket(self):
        """
        Create a new ticket and save it to the file.
        """
        signal = self.signal_input.text().strip()
        description = self.description_input.text().strip()
        severity = self.severity_input.text().strip()

        if not signal or not description or not severity:
            QMessageBox.warning(self, "Input Error", "All fields (Signal, Description, Severity) are required!")
            return

        if severity not in ["1", "2", "3"]:
            QMessageBox.warning(self, "Input Error", "Severity must be 1, 2, or 3.")
            return

        ticket_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add ticket to internal list
        ticket = {
            "Ticket_ID": ticket_id,
            "Timestamp": timestamp,
            "Signal": signal,
            "Severity": int(severity),
            "Status": "Open",
        }
        self.tickets.append(ticket)
        self.save_tickets()

        # Add ticket to the table
        row_position = self.ticket_table.rowCount()
        self.ticket_table.insertRow(row_position)
        self.ticket_table.setItem(row_position, 0, QTableWidgetItem(ticket_id))
        self.ticket_table.setItem(row_position, 1, QTableWidgetItem(timestamp))
        self.ticket_table.setItem(row_position, 2, QTableWidgetItem(signal))
        self.ticket_table.setItem(row_position, 3, QTableWidgetItem(severity))
        self.ticket_table.setItem(row_position, 4, QTableWidgetItem("Open"))

        # Update Dashboard
        self.update_dashboard()

        # Clear inputs
        self.signal_input.clear()
        self.description_input.clear()
        self.severity_input.clear()

    def update_dashboard(self):
        """Updates the dashboard with the latest ticket counts."""
        severity_count = {1: 0, 2: 0, 3: 0}

        for ticket in self.tickets:
            severity_count[ticket["Severity"]] += 1

        for severity, label in self.severity_labels.items():
            label.setText(f"Severity {severity}: {severity_count[severity]} tickets.")

    def save_tickets(self):
        """Saves the tickets to a JSON file."""
        try:
            with open(TICKET_FILE, "w") as file:
                json.dump(self.tickets, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save tickets: {e}")

    def load_tickets(self):
        """Loads tickets from the JSON file."""
        try:
            with open(TICKET_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def populate_ticket_table(self):
        """Populates the ticket table with saved tickets."""
        for ticket in self.tickets:
            row_position = self.ticket_table.rowCount()
            self.ticket_table.insertRow(row_position)
            self.ticket_table.setItem(row_position, 0, QTableWidgetItem(ticket["Ticket_ID"]))
            self.ticket_table.setItem(row_position, 1, QTableWidgetItem(ticket["Timestamp"]))
            self.ticket_table.setItem(row_position, 2, QTableWidgetItem(ticket["Signal"]))
            self.ticket_table.setItem(row_position, 3, QTableWidgetItem(str(ticket["Severity"])))
            self.ticket_table.setItem(row_position, 4, QTableWidgetItem(ticket["Status"]))


# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TickTrackApp()
    window.show()
    sys.exit(app.exec_())

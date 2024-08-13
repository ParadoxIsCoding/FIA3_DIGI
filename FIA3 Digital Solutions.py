import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class DataBreachTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Breach Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.conn = None
        self.cursor = None
        self.setup_database()
        self.setup_ui()

    def setup_ui(self):
        # Input fields
        input_layout = QHBoxLayout()

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location")
        self.breach_type_input = QLineEdit()
        self.breach_type_input.setPlaceholderText("Breach Type")
        self.impact_input = QLineEdit()
        self.impact_input.setPlaceholderText("Impact")

        for input_field in (self.location_input, self.breach_type_input, self.impact_input):
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 5px;
                    background-color: white;
                    color: black;
                }
                QLineEdit:focus {
                    border: 1px solid #4CAF50;
                }
            """)
            input_layout.addWidget(input_field)

        self.add_button = QPushButton("Add Entry")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.add_entry)
        input_layout.addWidget(self.add_button)

        self.layout.addLayout(input_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Location", "Breach Type", "Impact"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
                color: black;
            }
        """)
        self.layout.addWidget(self.table)

        self.load_data()

    def setup_database(self):
        self.conn = sqlite3.connect("data_breaches.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS breaches (
                id INTEGER PRIMARY KEY,
                location TEXT,
                breach_type TEXT,
                impact TEXT
            )
        """)
        self.conn.commit()

    def add_entry(self):
        location = self.location_input.text()
        breach_type = self.breach_type_input.text()
        impact = self.impact_input.text()

        if location and breach_type and impact:
            self.cursor.execute("INSERT INTO breaches (location, breach_type, impact) VALUES (?, ?, ?)",
                                (location, breach_type, impact))
            self.conn.commit()

            self.location_input.clear()
            self.breach_type_input.clear()
            self.impact_input.clear()

            self.load_data()

    def load_data(self):
        self.cursor.execute("SELECT location, breach_type, impact FROM breaches")
        data = self.cursor.fetchall()

        self.table.setRowCount(len(data))
        for row, (location, breach_type, impact) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(location))
            self.table.setItem(row, 1, QTableWidgetItem(breach_type))
            self.table.setItem(row, 2, QTableWidgetItem(impact))

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataBreachTracker()
    window.show()
    sys.exit(app.exec())
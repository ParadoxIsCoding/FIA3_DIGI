# FIA3 Digital Solutions, Taha Salman, 2024
import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QSize

class LoginScreen(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f0f0f0;")
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        for widget in (self.username_input, self.password_input, login_button):
            widget.setFixedSize(200, 30)
            central_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        central_layout.addSpacing(20)
        main_layout.addWidget(central_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
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
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def login(self):
        self.on_login()

class DataBreachTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Breach Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginScreen(self.show_main_screen)
        self.main_screen = QWidget()

        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.main_screen)

        self.conn = None
        self.cursor = None
        self.setup_database()
        self.setup_main_ui()

    def show_main_screen(self):
        self.central_widget.setCurrentWidget(self.main_screen)

    def setup_main_ui(self):
        layout = QVBoxLayout(self.main_screen)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_entries)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Input fields
        input_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location")
        self.breach_type_input = QLineEdit()
        self.breach_type_input.setPlaceholderText("Breach Type")
        self.impact_input = QLineEdit()
        self.impact_input.setPlaceholderText("Impact")

        for input_field in (self.location_input, self.breach_type_input, self.impact_input):
            input_layout.addWidget(input_field)

        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Location", "Breach Type", "Impact"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Apply styles
        self.main_screen.setStyleSheet("""
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
        self.display_data(self.cursor.fetchall())

    def search_entries(self):
        search_query = self.search_input.text().lower()
        self.cursor.execute("SELECT location, breach_type, impact FROM breaches")
        all_data = self.cursor.fetchall()
        
        filtered_data = [
            row for row in all_data
            if search_query in row[0].lower()
            or search_query in row[1].lower()
            or search_query in row[2].lower()
        ]
        
        self.display_data(filtered_data)

    def display_data(self, data):
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
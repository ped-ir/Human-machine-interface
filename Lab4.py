import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class StudentInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("lab4")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        # Прізвище, ім'я та по батькові
        full_name_label = QLabel("Педь Ігор Русланович")
        full_name_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(full_name_label)

        # Номер групи
        group_label = QLabel("К-121 20")
        group_label.setStyleSheet("color: purple; font-style: italic;")
        layout.addWidget(group_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentInfo()
    window.show()
    sys.exit(app.exec_())

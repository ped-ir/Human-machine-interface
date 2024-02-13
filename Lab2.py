import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QRadioButton, QSpinBox
import numpy as np

class FunctionCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('lab2')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Function selection
        function_layout = QHBoxLayout()
        self.function_label = QLabel('Виберіть функцію:')
        self.sin_cos_radio = QRadioButton('y = cos(2x) - 5sin(x) - 3')
        self.exp_radio = QRadioButton('y = 7^(1+x^3) - 4^(1-x^6)')
        function_layout.addWidget(self.function_label)
        function_layout.addWidget(self.sin_cos_radio)
        function_layout.addWidget(self.exp_radio)

        # Interval input
        interval_layout = QHBoxLayout()
        self.start_spinbox = QDoubleSpinBox()
        self.start_spinbox.setSingleStep(0.1)
        self.start_spinbox.setMaximum(100)
        self.end_spinbox = QDoubleSpinBox()
        self.end_spinbox.setSingleStep(0.1)
        self.end_spinbox.setMaximum(100)
        self.points_spinbox = QSpinBox()
        self.points_spinbox.setMinimum(2)
        interval_layout.addWidget(QLabel('Початок:'))
        interval_layout.addWidget(self.start_spinbox)
        interval_layout.addWidget(QLabel('Кінець:'))
        interval_layout.addWidget(self.end_spinbox)
        interval_layout.addWidget(QLabel('Точок:'))
        interval_layout.addWidget(self.points_spinbox)

        # Calculate button
        self.calculate_button = QPushButton('Обчислити')
        self.calculate_button.clicked.connect(self.calculate)

        # Table to display results
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['x', 'y'])
        layout.addLayout(function_layout)
        layout.addLayout(interval_layout)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def calculate(self):
        if self.sin_cos_radio.isChecked():
            func = lambda x: np.cos(2*x) - 5*np.sin(x) - 3
        elif self.exp_radio.isChecked():
            func = lambda x: 7**(1 + x**3) - 4**(1 - x**6)
        else:
            return

        start = self.start_spinbox.value()
        end = self.end_spinbox.value()
        points = self.points_spinbox.value()

        if end <= start:
            self.show_error_message("Кінець інтервалу повинен бути більшим за початок.")
            return

        try:
            x_values = np.linspace(start, end, points)
            y_values = func(x_values)
            self.display_results(x_values, y_values)
        except Exception as e:
            self.show_error_message(str(e))

    def display_results(self, x_values, y_values):
        self.table.setRowCount(len(x_values))
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            self.table.setItem(i, 0, QTableWidgetItem(str(x)))
            self.table.setItem(i, 1, QTableWidgetItem(str(y)))

    def show_error_message(self, message):
        QMessageBox.critical(self, 'Помилка', message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FunctionCalculator()
    window.show()
    sys.exit(app.exec_())

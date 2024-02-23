import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QMessageBox
import numpy as np
import pyqtgraph as pg

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def plot_function(self, x, y, color='b', line_width=2):
        self.plot_widget.clear()
        self.plot_widget.plot(x, y, pen=pg.mkPen(color=color, width=line_width))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("lab3")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.function_label = QLabel("Виберіть функцію:")
        self.function_combo = QComboBox()
        self.function_combo.addItems(["y = cos(2*x) - 5*sin(x) - 3", "y = 7^(1+x^3) - 4^(1-x^6)"])

        self.interval_start_label = QLabel("Початок інтервалу:")
        self.interval_start_input = QLineEdit()
        self.interval_start_input.setText("-10")  
        self.interval_end_label = QLabel("Кінець інтервалу:")
        self.interval_end_input = QLineEdit()
        self.interval_end_input.setText("10")  
        self.points_label = QLabel("Кількість точок:")
        self.points_input = QLineEdit()
        self.points_input.setText("1000")  

        self.plot_widget = PlotWidget()

        self.plot_button = QPushButton("Побудувати графік")
        self.plot_button.clicked.connect(self.plot_graph)

        form_layout = QFormLayout()
        form_layout.addRow(self.function_label, self.function_combo)
        form_layout.addRow(self.interval_start_label, self.interval_start_input)
        form_layout.addRow(self.interval_end_label, self.interval_end_input)
        form_layout.addRow(self.points_label, self.points_input)

        input_layout = QVBoxLayout()
        input_layout.addLayout(form_layout)
        input_layout.addWidget(self.plot_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.plot_widget)

        self.layout.addLayout(main_layout)

    def plot_graph(self):
        try:
            selected_function = self.function_combo.currentText()
            interval_start = float(self.interval_start_input.text())
            interval_end = float(self.interval_end_input.text())
            num_points = int(self.points_input.text())

            if interval_end <= interval_start:
                raise ValueError("Кінець інтервалу повинен бути більшим за початок.")

            x = np.linspace(interval_start, interval_end, num_points)
            if selected_function == "y = cos(2*x) - 5*sin(x) - 3":
                y = np.cos(2*x) - 5*np.sin(x) - 3
            elif selected_function == "y = 7^(1+x^3) - 4^(1-x^6)":
                y = 7**(1+x**3) - 4**(1-x**6)

            self.plot_widget.plot_function(x, y)

        except ValueError as ve:
            QMessageBox.critical(self, "Помилка", str(ve))
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

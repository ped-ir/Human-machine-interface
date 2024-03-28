import sys
from PySide6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QWidget, QVBoxLayout
from PySide6.QtGui import QColor, QBrush, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt
from functools import partial

class CustomRectItem(QGraphicsRectItem):
    def __init__(self, color, width, height, corner_radius=0, texts=None, text_colors=None, font_sizes=None, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, width, height)  # Установка размера прямоугольника
        self.color = color
        self.corner_radius = corner_radius
        self.texts = texts if texts else []
        self.text_colors = text_colors if text_colors else []
        self.font_sizes = font_sizes if font_sizes else []

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.NoPen))

        if self.corner_radius > 0:
            path = QPainterPath()
            path.addRoundedRect(self.rect(), self.corner_radius, self.corner_radius)
            painter.drawPath(path)
        else:
            painter.drawRect(self.rect())

        for text, color, font_size in zip(self.texts, self.text_colors, self.font_sizes):
            painter.setPen(QPen(color))
            font = QFont("Arial", font_size)
            if 'https://www.qt.io/' in text:
                font.setUnderline(True)
            elif 'Педь Ігор Русланович' in text:
                font.setBold(True)
            elif 'Солнце,ветер,река,песок,море' in text:
                font.setItalic(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, text)

class CustomScene(QGraphicsScene):
    def __init__(self, colors, positions, rotations, texts, text_colors, font_sizes, corner_radius=None, parent=None):
        super().__init__(parent)
        self.colors = colors
        self.positions = positions
        self.rotations = rotations
        self.texts = texts
        self.text_colors = text_colors
        self.font_sizes = font_sizes
        self.corner_radius = corner_radius if corner_radius else [0] * len(colors)
        self.setupScene()

    def setupScene(self):
        for color, pos, rotation, text, text_color, font_size, radius in zip(self.colors, self.positions, self.rotations, self.texts, self.text_colors, self.font_sizes, self.corner_radius):
            rect = CustomRectItem(color, 200, 200, radius, text, text_color, font_size)
            rect.setPos(*pos)
            rect.setRotation(rotation)
            self.addItem(rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    colors = [
        QColor(136, 0, 0),  # Top-left
        QColor(255, 0, 0),  # Top-right
        QColor(0, 255, 0),  # Bottom-left
        QColor(0, 136, 0),  # Bottom-right
        QColor(65, 105, 225), # Center
        QColor(255, 255, 0), # Yellow
        QColor(255, 127, 0),  # Orange
        QColor(255, 0, 255),  # Violet
        QColor(75, 0, 130),  # Indigo
        QColor(0, 0, 255),  # Blue
        QColor(0, 255, 255),  # Cyan
        QColor(0, 128, 0)  # Green (removed white)
    ]
    positions = [
        (0, 0),          # Top-left
        (320, 0),        # Top-right
        (0, 240),        # Bottom-left
        (320, 240),      # Bottom-right
        (120, 220),       # Center
        (240, 220),      # Yellow square
        (480, 220),      # Orange square
        (480, 220),      # Violet square
        (480, 220),      # Indigo square
        (480, 220),      # Blue square
        (480, 220),      # Cyan square
        (480, 220)      # Green square
    ]
    rotations = [0, 0, 0, 0, -45]
    texts = [
        ["к121-20"],
        ["https://www.github.com/"],
        ["color: '#00FF00'"],
        ["Солнце,ветер,река,песок,море"],
        ["Педь Ігор Русланович"]
    ]
    text_colors = [
        [QColor(Qt.black)],
        [QColor(Qt.black)],
        [QColor(Qt.black)],
        [QColor(Qt.black)] * 5,
        [QColor(Qt.black)]
    ]
    font_sizes = [
        [10],
        [10],
        [10],
        [10] * 5,
        [10]
    ]
    corner_radius = [0, 0, 0, 0, 20]

    scene = CustomScene(colors, positions, rotations, texts, text_colors, font_sizes, corner_radius)

    view = QGraphicsView(scene)
    view.resize(640, 480)

    button = QPushButton("Close Program")
    button.clicked.connect(app.quit)

    def update_color(scene, color):
        for item in scene.items():
            if isinstance(item, CustomRectItem) and "Педь Ігор Русланович" in item.texts[0]:
                item.color = color
                scene.update()
                break

    palette_layout = QHBoxLayout()  # Change to horizontal layout
    palette_widget = QWidget()

    rainbow_colors = colors[5:]  # Extract rainbow colors
    for color in rainbow_colors:
        square = QPushButton()
        square.setFixedSize(15, 15)
        square.setStyleSheet(f"background-color: {color.name()}")
        square.clicked.connect(partial(update_color, scene, color))
        palette_layout.addWidget(square)

    palette_widget.setLayout(palette_layout)

    layout = QVBoxLayout()
    layout.addWidget(view)
    layout.addWidget(palette_widget)
    layout.addWidget(button)

    widget = QWidget()
    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec())

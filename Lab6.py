import sys
from PySide6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen, QPainterPath, QFont

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
            elif 'Lorem ipsum' in text:
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
        QColor(136, 0, 0),   # Top-left
        QColor(255, 0, 0),   # Top-right
        QColor(0, 255, 0),   # Bottom-left
        QColor(0, 136, 0),   # Bottom-right
        QColor(65, 105, 225)  # Center
    ]
    positions = [
        (0, 0),           # Top-left
        (320, 0),         # Top-right
        (0, 240),         # Bottom-left
        (320, 240),       # Bottom-right
        (120, 220)        # Center
    ]
    rotations = [0, 0, 0, 0, -45]
    texts = [
        ["K121-20"],
        ["https://www.bupbip.com"],
        ["color: '#00FF00'"],
        ["Lorem ipsum"],
        ["Педь Ігор Русланович"]
    ]
    text_colors = [
        [QColor(Qt.black)],
        [QColor(Qt.black)],
        [QColor(Qt.black)],
        [QColor(Qt.black)] * 5,  # Черный цвет для каждого текста
        [QColor(Qt.black)]
    ]
    font_sizes = [
        [10],
        [10],
        [10],
        [10] * 5,  # Размер шрифта 10 для каждого текста
        [10]
    ]
    corner_radius = [0, 0, 0, 0, 20]   # Радиус закругления только для центрального квадрата

    scene = CustomScene(colors, positions, rotations, texts, text_colors, font_sizes, corner_radius)
    view = QGraphicsView(scene)
    view.resize(640, 480)
    view.show()

    sys.exit(app.exec())

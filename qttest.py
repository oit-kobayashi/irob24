import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class MyCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(640, 480)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.text = QLabel("hello, world")
        self.canvas = MyCanvas(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.canvas)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.eraseRect(0, 0, 100, 100)
        p.setBrush(QColor(0x00ffff))
        p.drawLine(0, 0, 200, 100)

        
app =QApplication([])
w = MyWidget()
w.resize(800, 600)
w.show()

app.exec()

#  sudo apt update
#  sudo apt install libqt6desiner6

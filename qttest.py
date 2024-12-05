import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("hello, world")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)

app = QtWidgets.QApplication([])
w = MyWidget()
w.resize(800, 600)
w.show()

app.exec()

#  sudo apt update
#  sudo apt install libqt6desiner6

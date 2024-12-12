import sys
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from mobrob import Robot

W = 800  # 画面の幅(pixel)
H = 800
Wr = 10  # 実際の幅(m)
Hr = 10

# 実際の座標をピクセル座標に変換する関数
def _x(x):
    return x * W / Wr + W / 2

def _y(y):
    return -y * H / Hr + H / 2

def _s(r):  # 幅を基準にスケール変換
    return r * W / Wr


class Canvas(QWidget):
    def __init__(self, r):
        self.robot = r
        super().__init__()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        x = self.robot.p[0, 0]
        y = self.robot.p[1, 0]
        t = self.robot.p[2, 0]
        r = self.robot.b / 2
        vx = 0.5 * np.cos(t)
        vy = 0.5 * np.sin(t)
        painter.drawEllipse(QPoint(_x(x), _y(y)),
                            _s(r), _s(r))
        painter.drawLine(_x(x), _y(y),
                         _x(x + vx), _y(y + vy))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.robot = Robot()
        
        layoutH = QHBoxLayout(self)
        self.canvas = Canvas(self.robot)
        self.canvas.resize(W, H)
        self.btnQ = QPushButton("QUIT")
        self.btnQ.clicked.connect(lambda: sys.exit(0))
        right = QWidget()
        layoutV = QVBoxLayout(right)
        layoutH.addWidget(self.canvas)
        layoutH.addWidget(right)
        layoutV.addWidget(QLabel("right-upper"))
        layoutV.addWidget(self.btnQ)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainW = App()
    mainW.resize(960, 800)
    mainW.show()
    app.exec()
    

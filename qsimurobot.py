import sys
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from mobrob import Robot


class Canvas(QWidget):
    W = 800  # 画面の幅(pixel)
    H = 800
    scale = W / 10  # スケールファクタの初期値 (幅基準)
    # 実際の座標をピクセル座標に変換する関数
    def _x(self, x):
        return x * self.scale + self.W / 2

    def _y(self, y):
        return -y * self.scale + self.H / 2

    def _s(self, r):  # 幅を基準にスケール変換
        return r * self.scale

    def updateScale(self, mag):
        self.scale = self.scale * mag
        return self.scale

    def __init__(self, r):
        self.robot = r
        super().__init__()
        self.setFixedSize(self.W, self.H)

    def _drawRobot(self, p, stroke: QColor, fill: QColor):
        painter = QPainter(self)
        pen = QPen(stroke, 1.5)
        painter.setPen(pen)
        painter.setBrush(fill)
        x = p[0, 0]
        y = p[1, 0]
        t = p[2, 0]
        r = self.robot.b / 2
        # draw robot
        painter.translate(self._x(x), self._y(y))
        painter.rotate(-t * 180 / np.pi)
        painter.drawEllipse(QPoint(0,0), self._s(r), self._s(r))
        painter.drawLine(0, 0, self._s(0.5), 0)  # direction
        painter.drawRects([QRect(self._s(-0.1), self._s(r), self._s(0.2), self._s(0.05))])
        painter.drawRects([QRect(self._s(-0.1), self._s(-r), self._s(0.2), self._s(-0.05))])
        
        
    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBackground(Qt.black)
        painter.eraseRect(0, 0, self.W, self.H)
        self._drawRobot(self.robot.p0, Qt.white, QColor(70, 70, 70))
        self._drawRobot(self.robot.p, Qt.cyan, QColor(130, 180, 180, 180))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.robot = Robot()

        # setup GUI
        layoutH = QHBoxLayout(self)
        self.canvas = Canvas(self.robot)
        self.btnQ = QPushButton("QUIT")
        self.btnZdec = QPushButton("zoom-")
        self.btnZinc = QPushButton("zoom+")
        self.btnQ.clicked.connect(lambda: sys.exit(0))
        self.btnZdec.clicked.connect(lambda: self.canvas.updateScale(0.9))
        self.btnZinc.clicked.connect(lambda: self.canvas.updateScale(1.1))
        self.labelX = QLabel("x")
        self.labelY = QLabel("y")
        self.labelT = QLabel("th")
        right = QWidget()
        layoutV = QVBoxLayout(right)
        layoutH.addWidget(self.canvas)
        layoutH.addWidget(right)
        infoFrame = QFrame()
        infoFrame.setFrameShape(QFrame.StyledPanel)
        layoutV.addWidget(infoFrame)
        layoutV.addWidget(self.btnZinc)
        layoutV.addWidget(self.btnZdec)
        layoutV.addWidget(self.btnQ)
        layoutV2 = QVBoxLayout(infoFrame)
        layoutV2.addWidget(self.labelX)
        layoutV2.addWidget(self.labelY)
        layoutV2.addWidget(self.labelT)
        layoutV2.addStretch()
        

        # setup timer
        self.timer = QTimer()
        self.timer.setInterval(1000 // 60) # 60 fps
        self.timer.timeout.connect(self.step)
        self.timer.start()


    def step(self):  # interval function
        self.robot.move(0.01, 0.015)
        self.update()
        # update info labels
        x = self.robot.p[0, 0]
        y = self.robot.p[1, 0]
        t = self.robot.p[2, 0]
        self.labelX.setText(f"x={x:.4f}")
        self.labelY.setText(f"y={y:.4f}")
        self.labelT.setText(f"th={t:.4f}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainW = App()
    mainW.show()
    app.exec()
    

import sys
import numpy as np
import numpy.linalg as la
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from mobrob import Robot


class Canvas(QWidget):
    W = 800  # 画面の幅(pixel)
    H = 800
    track = False   # ロボットを中心に描画するか?
    scale = W / 10  # スケールファクタの初期値 (幅基準)

    def setTrack(self, t: bool) -> None:
        self.track = t
    
    # 実際の座標をピクセル座標に変換する関数
    def _x(self, x) -> int:
        if self.track:
            x = x - self.robot.p0[0, 0]
        return int(x * self.scale + self.W / 2)

    def _y(self, y) -> int:
        if self.track:
            y = y - self.robot.p0[1, 0]
        return int(-y * self.scale + self.H / 2)

    def _s(self, r):  # 幅を基準にスケール変換
        return r * self.scale

    def updateScale(self, mag):
        self.scale = self.scale * mag

    def __init__(self, r):
        self.robot = r
        super().__init__()
        self.setFixedSize(self.W, self.H)


    def _drawBelief(self,
                    p: np.array,     # pose (expectation)
                    sigma: np.array, # sigma (covariance matrix)
                    stroke: QColor):
        painter = QPainter(self)
        painter.setPen(QPen(stroke, 1))
        x = p[0, 0]
        y = p[1, 0]
        # t = p[2, 0]
        painter.translate(self._x(x), self._y(y))

        sigma_xy = sigma[0:2, 0:2]
        sigma_t  = np.sqrt(sigma[2, 2])
        w, v = la.eig(sigma_xy)
        p0x = v[0, 0]
        p0y = v[1, 0]
        angle = -np.atan2(p0y, p0x) * 180 / np.pi
        painter.save()
        painter.rotate(angle)
        painter.drawEllipse(QPoint(0, 0), self._s(float(np.sqrt(w[0]))), self._s(float(np.sqrt(w[1]))))

        painter.restore()
        painter.rotate(-p[2, 0] * 180 / np.pi)
        painter.drawLine(0, 0, self._s(float(np.cos(sigma_t))), self._s(float(np.sin(sigma_t))))
        painter.drawLine(0, 0, self._s(float(np.cos(sigma_t))), self._s(float(np.sin(-sigma_t))))
        painter.drawLines([
            QPoint(self._s(float(np.cos(sigma_t))), self._s(float(np.sin(sigma_t)))),
            QPoint(0, 0),
            QPoint(self._s(float(np.cos(sigma_t))), self._s(float(np.sin(-sigma_t))))])

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
        painter.setPen(QPen(Qt.green, 0.5))
        # grid
        ix, iy = list(self.robot.p0[0:2, 0].astype(np.int32))
        for i in range(-20, 20):
            painter.drawLine(self._x(ix + i), self._y(iy -20), self._x(ix + i), self._y(iy + 20))
            painter.drawLine(self._x(ix - 20), self._y(iy + i), self._x(ix + 20), self._y(iy + i))
        painter.setPen(QPen(Qt.green, 1))
        painter.drawLine(self._x(0), self._y(-20), self._x(0), self._y(20))
        painter.drawLine(self._x(-20), self._y(0), self._x(20), self._y(0))
        #
        self._drawRobot(self.robot.p0, Qt.white, QColor(70, 70, 70))
        self._drawBelief(self.robot.p, self.robot.sigma_p, QColor(130, 180, 180, 180))
        self._drawRobot(self.robot.p, Qt.cyan, QColor(130, 180, 180, 180))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.robot = Robot()
        self.dsl = 0.002
        self.dsr = 0.00111111111
        self.t = 0    # time counter

        # setup GUI
        layoutH = QHBoxLayout(self)
        self.canvas = Canvas(self.robot)
        self.btnQ = QPushButton("QUIT")
        self.btnP = QPushButton("pause")
        self.btnZdec = QPushButton("zoom-")
        self.btnZinc = QPushButton("zoom+")
        self.toggleTrack = QToolButton()
        self.toggleTrack.setText("track")
        self.toggleTrack.setCheckable(True)
        self.toggleTrack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toggleTrack.clicked.connect(lambda: self.canvas.setTrack(self.toggleTrack.isChecked()))
        self.btnQ.clicked.connect(lambda: sys.exit(0))
        self.btnP.clicked.connect(self.pauseResume)
        self.btnZdec.clicked.connect(lambda: self.canvas.updateScale(0.9) or self.update())
        self.btnZinc.clicked.connect(lambda: self.canvas.updateScale(1.1) or self.update())
        self.labelX = QLabel("x")
        self.labelY = QLabel("y")
        self.labelT = QLabel("th")
        self.labelTime = QLabel("time")
        right = QWidget()
        layoutV = QVBoxLayout(right)
        layoutH.addWidget(self.canvas)
        layoutH.addWidget(right)
        infoFrame = QFrame()
        infoFrame.setFrameShape(QFrame.StyledPanel)
        layoutV.addWidget(infoFrame)
        layoutV.addWidget(self.toggleTrack)
        layoutV.addWidget(self.btnZinc)
        layoutV.addWidget(self.btnZdec)
        layoutV.addWidget(self.btnP)
        layoutV.addWidget(self.btnQ)
        layoutV2 = QVBoxLayout(infoFrame)
        layoutV2.addWidget(self.labelTime)
        layoutV2.addWidget(self.labelX)
        layoutV2.addWidget(self.labelY)
        layoutV2.addWidget(self.labelT)
        layoutV2.addStretch()
        

        # setup timer
        self.timer = QTimer()
        self.timer.setInterval(1000 // 60) # 60 fps
        self.timer.timeout.connect(self.step)
        self.timer.start()

    def pauseResume(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def keyPressEvent(self, e: QKeyEvent):
        print(e, e.key())
        if e.key() == Qt.Key.Key_Left:
            self.dsl += -0.0005
            self.dsr +=  0.0005
        elif e.key() == Qt.Key.Key_Right:
            self.dsr += -0.0005
            self.dsl +=  0.0005
        elif e.key() == Qt.Key.Key_Up:
            self.dsr +=  0.0005
            self.dsl +=  0.0005
        elif e.key() == Qt.Key.Key_Down:
            self.dsr += -0.0005
            self.dsl += -0.0005
        

    def step(self):  # interval function
        self.t += 1
        self.robot.move(self.dsr, self.dsl)
        if self.t % 600 == 0:
            self.robot.perception(
                self.robot.p0 + np.random.randn(3) * [1, 1, 0.25],
                np.diag([2, 2, 0.5**2])
            )
        self.update()
        # update info labels
        x = self.robot.p[0, 0]
        y = self.robot.p[1, 0]
        t = self.robot.p[2, 0]
        self.labelX.setText(f"x={x:.4f}")
        self.labelY.setText(f"y={y:.4f}")
        self.labelT.setText(f"th={t:.4f}")
        self.labelTime.setText(f"T={self.t:8d}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainW = App()
    mainW.setFocus()
    mainW.show()
    app.exec()
    

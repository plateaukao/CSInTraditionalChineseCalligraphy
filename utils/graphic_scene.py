# coding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

        self.lastPoint = None
        self.endPoint = None

        self.points = []
        self.strokes = []
        self.T_DISTANCE = 10

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        """
            Mouse press clicked!
        :param event:
        :return:
        """
        pen = QPen(Qt.red)
        brush = QBrush(Qt.red)
        x = event.scenePos().x()
        y = event.scenePos().y()

        if len(self.points) == 0:
            self.addEllipse(x, y, 2, 2, pen, brush)
            self.endPoint = event.scenePos()
        else:
            x0 = self.points[0][0]
            y0 = self.points[0][1]

            dist = math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0))
            if dist < self.T_DISTANCE:
                # end and close point
                pen_ = QPen(Qt.green)
                brush_ = QBrush(Qt.green)
                self.addEllipse(x0, y0, 2, 2, pen_, brush_)
                self.endPoint = event.scenePos()
                x = x0; y = y0
            else:
                self.addEllipse(x, y, 4, 4, pen, brush)
                self.endPoint = event.scenePos()
        self.points.append((x, y))

    def mouseReleaseEvent(self, event):
        """
            Mouse release event!
        :param event:
        :return:
        """
        pen = QPen(Qt.red)

        if self.lastPoint is not None and self.lastPoint is not None:
            self.addLine(self.endPoint.x(), self.endPoint.y(), self.lastPoint.x(), self.lastPoint.y(), pen)

        self.lastPoint = self.endPoint
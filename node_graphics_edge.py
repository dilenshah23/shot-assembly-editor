from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from node_socket import *

class NodeGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        
        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0 ,0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, item, widget=None):
        self.updatePath()
        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)

        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        

    def updatePath(self):
        # Will handle drawing QPainterPath from Point A to Point B
        raise NotImplemented('This method has to be overriden in a child class')


class NodeGraphicsEdgeDirect(NodeGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class NodeGraphicsEdgeBezier(NodeGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        #if s[0] > d[0]: dist *= -1

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1],
                    self.posDestination[0], self.posDestination[1])
        self.setPath(path)
        
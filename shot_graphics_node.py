from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ShotGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)
        self._title_font.setBold(True)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 50
        self._padding = 9.0
        self.socket_height = 35

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor('#FF313131'))
        self._brush_background = QBrush(QColor("#E3212121"))

        # init title
        self.__init_title__()     
        self.title = self.node.title

        # init sockets
        self.__init_sockets__()

        # init content
        self.__init_content__()
        
        self.__init_ui__()


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        for node in self.scene().scene.nodes:
            if node.graphics_node.isSelected():
                node.updateConnectedEdges()

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        return QRectF(  0,
                        0,
                        self.width,
                        self.height
                        ).normalized()

    def __init_ui__(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def __init_title__(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.width/4 + self._padding, self.title_height/4)
        self.title_item.setTextWidth(
            self.width - 2 * self._padding
        )
    
    def __init_content__(self):
        self.graphic_content = QGraphicsProxyWidget(self)
        print(self.content)
        self.content.setGeometry(self.edge_size, self.edge_size, 
                                    self.width - 2*self.edge_size, self.height)
        print(self.height-2*self.edge_size-self.title_height)

        self.graphic_content.setWidget(self.content)

    def __init_sockets__(self):
        pass

    def paint(self, painter, item, widget=None):

        #title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        #content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRect(0,self.title_height, self.width, self.height-self.title_height-self.socket_height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        #socket
        socket_content = QPainterPath()
        socket_content.setFillRule(Qt.WindingFill)
        socket_content.addRoundedRect(0, self.height - self.socket_height, self.width, self.socket_height, self.edge_size, self.edge_size)
        socket_content.addRect(0, self.height - self.socket_height, self.edge_size, self.edge_size)
        socket_content.addRect(self.width - self.edge_size, self.height-self.socket_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(socket_content.simplified())

        #outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())


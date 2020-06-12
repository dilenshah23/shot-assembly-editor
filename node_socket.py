from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from node_graphics_socket import NodeGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type


        self.graphic_socket = NodeGraphicsSocket(self, self.socket_type)

        self.graphic_socket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None


    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None


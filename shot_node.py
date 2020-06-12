from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shot_graphics_node import ShotGraphicsNode
from node_content_widget import NodeContentWidget
from node_socket import *

DEBUG = False

class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene
        self.title = title

        self.content = NodeContentWidget()
        self.graphics_node = ShotGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphics_scene.addItem(self.graphics_node)

        self.socket_spacing = 23

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTOM, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.graphics_node.pos()

    def setPos(self, x, y):
        self.graphics_node.setPos(x, y)

    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.graphics_node.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.graphics_node.height - self.graphics_node._padding - self.graphics_node.edge_size - index * self.socket_spacing
        else: 
            # start from top
            y = self.graphics_node.title_height + self.graphics_node._padding + self.graphics_node.edge_size + index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        if DEBUG: print("> Removing Node", self)
        if DEBUG: print("> remove all edges from sockets")
        for socket in (self.inputs+self.outputs):
            if socket.hasEdge():
                if DEBUG: print("     - removing from socket: %s edge: %s" % (socket, socket.edge))
                socket.edge.remove()
        if DEBUG: print("> Removing graphic node")
        self.scene.graphics_scene.removeItem(self.graphics_node)
        self.graphics_node = None
        if DEBUG: print("> Removing graphic node from the scene")
        self.scene.removeNode(self)
        if DEBUG: print("> everything was removed properly")

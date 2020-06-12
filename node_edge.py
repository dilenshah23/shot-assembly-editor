from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG=False

class Edge():
    def __init__(self, scene, start_socket, end_socket, edgeType=EDGE_TYPE_DIRECT):
        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.graphic_edge = NodeGraphicsEdgeDirect(self) if edgeType==EDGE_TYPE_DIRECT else NodeGraphicsEdgeBezier(self)

        self.updatePositions()

        self.scene.graphics_scene.addItem(self.graphic_edge)
        self.scene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphics_node.pos().x()
        source_pos[1] += self.start_socket.node.graphics_node.pos().y()
        self.graphic_edge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphics_node.pos().x()
            end_pos[1] += self.end_socket.node.graphics_node.pos().y()
            self.graphic_edge.setDestination(*end_pos)
        else:
            self.graphic_edge.setDestination(*source_pos)

        self.graphic_edge.update()
        
    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        if DEBUG: print("> Removing Edge", self)
        if DEBUG: print("> remove edge from all sockets")
        self.remove_from_sockets()
        if DEBUG: print("> remove graphic edge")
        self.scene.graphics_scene.removeItem(self.graphic_edge)
        self.graphic_edge = None
        if DEBUG: print("> remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass
            if DEBUG: print("EXCEPTION:", e, type(e))
        if DEBUG: print(" - removed edge properly")
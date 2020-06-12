from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shot_graphics_scene import ShotGraphicsScene

class Scene():
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.scene_width = 2300
        self.scene_height = 2300

        self.__init_ui__()

    def __init_ui__(self):
        self.graphics_scene = ShotGraphicsScene(self)
        self.graphics_scene.setGraphicsSceneRect(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, node):
        self.edges.remove(node)
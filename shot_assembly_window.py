from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shot_scene import Scene
from shot_node import Node
from shot_graphics_view import ShotGraphicsView
from node_edge import Edge, EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER

class ShotAssemblyWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = "./qss/nodestyle.qss"
        self.loadStylesheet(self.stylesheet_filename)

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()

        self.addNodes()

        # Create graphics view
        self.view = ShotGraphicsView(self.scene.graphics_scene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Shot Editor")
        self.show()


    def loadStylesheet(self, filename):
        print ("Style Loading :", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def addNodes(self):
        node1 = Node(self.scene, "Skeleton", inputs=[0], outputs=[1])
        node2 = Node(self.scene, "Muscle", inputs=[0], outputs=[1])
        node3 = Node(self.scene, "Fascia/Fat", inputs=[0], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, -0)
        node3.setPos(200, -150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edgeType=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edgeType=EDGE_TYPE_BEZIER)
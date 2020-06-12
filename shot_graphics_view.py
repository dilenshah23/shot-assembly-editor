from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_edge import NodeGraphicsEdge
from node_graphics_socket import NodeGraphicsSocket

MODE_NOOPERATION = 1
MODE_EDGE_DRAG = 2
DEBUG = False
EDGE_DRAG_START_THRESHOLD = 10

class ShotGraphicsView(QGraphicsView):
    def __init__(self, graphics_scene, parent=None):
        super().__init__(parent)

        self.graphics_scene = graphics_scene
        self.__init_ui__()
        self.setScene(self.graphics_scene)

        self.mode = MODE_NOOPERATION

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 15]

    def __init_ui__(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), 
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), 
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), 
                                Qt.LeftButton, event.buttons() & Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):      
        item = self.getItemAtClick(event)

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if DEBUG: print("LMB Click on", item, self.debug_modifiers(event) )

        if hasattr(item, "node") or isinstance(item, NodeGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is NodeGraphicsSocket:
            if self.mode == MODE_NOOPERATION:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):

        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, NodeGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print("LMB Release + Shift on", item )
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            self.distanceBetweenClickAndReleaseIsOff(event)    
            if self.distanceBetweenClickAndReleaseIsOff:
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.graphic_edge.setDestination(pos.x(), pos.y())
            self.dragEdge.graphic_edge.update()
        
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Delete:
            self.deleteSelected()
        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        for item in self.graphics_scene.selectedItems():
            if isinstance(item, NodeGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ATL "
        return out

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart - Start Dragging edge')
        if DEBUG: print('View::edgeDragStart - assign Start Socket to:', item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.graphics_scene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart - dragEdge:', self.dragEdge)


    def edgeDragEnd(self, item):
        self.mode = MODE_NOOPERATION
        
        if type(item) is NodeGraphicsSocket:
            if item.socket != self.last_start_socket:
                if DEBUG: print('View::edgeDragEnd - previous edge', self.previousEdge)
                if item.socket.hasEdge():
                    item.socket.edge.remove()

                if DEBUG: print('View::edgeDragEnd - End Dragging edge', item.socket)
                if self.previousEdge is not None: self.previousEdge.remove()
                if DEBUG: print('View::edgeDragEnd - previous edge removed')
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                if DEBUG: print('View::edgeDragEnd - reassigned start & end sockets to drag edge')
                self.dragEdge.updatePositions()
                return True

        if DEBUG: print('View::edgeDragEnd - End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print('View::edgeDragEnd - about to set socket to previous edge:', self.previousEdge)
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print('View::edgeDragEnd - everything done')

    def distanceBetweenClickAndReleaseIsOff(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1/self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
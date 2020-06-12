from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class NodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__init_ui__()

    def __init_ui__(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.main_layout = QGridLayout()
        self.main_layout.setVerticalSpacing(15)

        self.name_label = QLabel("Name")
        self.name_edit = QLineEdit("Skeleton")
        self.main_layout.addWidget(self.name_label, 0,0,1,1)
        self.main_layout.addWidget(self.name_edit, 0,1,1,1)

        self.type_label = QLabel("Type")
        self.type_edit = QLineEdit("Skeleton")
        self.main_layout.addWidget(self.type_label, 1,0,1,1)
        self.main_layout.addWidget(self.type_edit, 1,1,1,1)

        self.asset_label = QLabel("Asset")
        self.asset_edit = QLineEdit()
        self.main_layout.addWidget(self.asset_label, 2,0,1,1)
        self.main_layout.addWidget(self.asset_edit, 2,1,1,1)

        self.tractor_label = QLabel("Tractor")
        self.tractor_combo = QComboBox()
        self.tractor_combo.addItems(["remote", "local"])
        self.main_layout.addWidget(self.tractor_label, 3,0,1,1)
        self.main_layout.addWidget(self.tractor_combo, 3,1,1,1)

        self.layout.addLayout(self.main_layout)
import sys
from PyQt5.QtWidgets import *

from shot_assembly_window import ShotAssemblyWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShotAssemblyWindow()
    sys.exit(app.exec_())
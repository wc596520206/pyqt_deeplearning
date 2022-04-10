

import sys
import os
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

from controller.p1 import p1
from controller.p2 import p2
from controller.p3 import p3

class c1(p1, p2,p3):
    def __init__(self):
        super(c1, self).__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = c1()
    ui.show()
    sys.exit(app.exec_())
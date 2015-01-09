import sys
from PySide import QtGui
from ibl_stuff.gui.explorer import Explorer


def show():
    w = Explorer(parent=QtGui.QApplication.activeWindow())
    w.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Explorer()
    w.show()
    sys.exit(app.exec_())

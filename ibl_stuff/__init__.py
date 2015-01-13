import sys
from PySide import QtGui
from ibl_stuff.gui.explorer import Explorer


def show():
    parent = QtGui.QApplication.activeWindow()
    w = None
    for child in parent.children():
        if not isinstance(child, Explorer):
            continue
        w = child
    if w is None:
        w = Explorer(parent)
    w.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Explorer()
    w.show()
    sys.exit(app.exec_())

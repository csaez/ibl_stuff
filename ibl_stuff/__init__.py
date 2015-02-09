import sys
from PySide import QtGui
from ibl_stuff.gui import Explorer
from ibl_stuff.libs import qt_helpers


def show():
    parent = qt_helpers.get_parent()
    w = qt_helpers.find_instance(parent, Explorer)
    if w is None:
        w = Explorer(parent)
    w.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Explorer()
    w.show()
    sys.exit(app.exec_())

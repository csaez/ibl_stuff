import sys
from PySide import QtGui
from ibl_stuff.gui import Explorer


def show():
    # get parent
    parent = QtGui.QApplication.activeWindow()
    _ = parent.parent()
    while _:
        parent = _
        _ = parent.parent()
    # find instance
    w = None
    for child in parent.children():
        if not isinstance(child, Explorer):
            continue
        w = child
    if w is None:
        w = Explorer(parent)
    # show
    w.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Explorer()
    w.show()
    sys.exit(app.exec_())

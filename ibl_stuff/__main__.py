import sys
from PySide import QtGui
import ibl_stuff


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = ibl_stuff.Explorer()
    w.show()
    sys.exit(app.exec_())

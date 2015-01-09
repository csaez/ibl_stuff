from PySide import QtGui
from ibl_stuff.api import get_ibls


class Card(QtGui.QWidget):

    labels = ("title", "type", "lighting", "comments")

    def __init__(self, ibl, *arg, **kwds):
        super(Card, self).__init__(*arg, **kwds)
        self.ibl_data = ibl
        self.init_ui()

    def init_ui(self):
        # init labels
        for each in self.labels:
            setattr(self, each, QtGui.QLabel())

        # set layout
        hbox = QtGui.QHBoxLayout()
        for x in (self.lighting, QtGui.QLabel("-"), self.type):
            hbox.addWidget(x)
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addLayout(hbox)
        vbox.addWidget(self.comments)
        self.setLayout(vbox)

        self.update()

    def update(self, ibl_data=None):
        if ibl_data is not None:
            self.ibl_data = ibl_data
        # update labels
        for x in self.labels:
            data = self.ibl_data.get(x) if x != "tags" else ",".join(x)
            getattr(self, x).setText(data)


class Explorer(QtGui.QMainWindow):

    def __init__(self, *arg, **kwds):
        super(Explorer, self).__init__(*arg, **kwds)
        title = type(self).__name__.replace("_", " ")
        self.setWindowTitle(title)
        self.init_ui()

    def init_ui(self):
        layout = QtGui.QVBoxLayout()
        for ibl in get_ibls():
            layout.addWidget(Card(ibl))
        w = QtGui.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

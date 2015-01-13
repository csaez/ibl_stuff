from PySide import QtGui
from ibl_stuff import api


class Preview(QtGui.QGraphicsView):

    def __init__(self, *arg, **kwds):
        super(Preview, self).__init__(*arg, **kwds)
        self.setScene(QtGui.QGraphicsScene())
        self.setFixedSize(250, 125)


class Card(QtGui.QWidget):

    labels = ("title", "type", "lighting", "comments")
    title = property(lambda s: s._fget("title"),
                     lambda s, x: s._fset("title", x))
    type = property(lambda s: s._fget("type"),
                    lambda s, x: s._fset("type", x))
    lighting = property(lambda s: s._fget("lighting"),
                        lambda s, x: s._fset("lighting", x))
    comments = property(lambda s: s._fget("comments"),
                        lambda s, x: s._fset("comments", x))

    def __init__(self, *arg, **kwds):
        super(Card, self).__init__()
        # init data
        for k, v in kwds.iteritems():
            if k in self.labels:
                setattr(self, "_" + k, v)
        # init ui
        self.init_ui()

    def _fget(self, arg):
        if hasattr(self, "_" + arg):
            return getattr(self, "_" + arg)
        return ""

    def _fset(self, arg, value):
        setattr(self, arg, value)
        self.update()

    def init_ui(self):
        self.ui_thumb = Preview()
        for each in self.labels:
            setattr(self, "ui_" + each, QtGui.QLabel())
        f = self.ui_title.font()
        f.setPointSize(f.pointSize() * 1.5)
        f.setBold(True)
        f.setCapitalization(QtGui.QFont.AllUppercase)
        self.ui_title.setFont(f)
        # set layout
        label_hbox = QtGui.QHBoxLayout()
        for x in (self.ui_lighting, QtGui.QLabel("-"), self.ui_type):
            label_hbox.addWidget(x)
        label_hbox.addStretch(1)
        label_vbox = QtGui.QVBoxLayout()
        label_vbox.addWidget(self.ui_title)
        label_vbox.addLayout(label_hbox)
        label_vbox.addWidget(self.ui_comments)
        label_vbox.addStretch(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.ui_thumb)
        hbox.addLayout(label_vbox)

        self.setLayout(hbox)
        self.update()

    def update(self):
        for x in self.labels:
            data = self._fget(x)
            getattr(self, "ui_" + x).setText(data)


class Explorer(QtGui.QMainWindow):

    def __init__(self, *arg, **kwds):
        super(Explorer, self).__init__(*arg, **kwds)
        title = "IBL Stuff - " + type(self).__name__.replace("_", " ")
        self.setWindowTitle(title)
        self.init_ui()

    def add_ibl(self, **kwds):
        item = QtGui.QListWidgetItem()
        c = Card(**kwds)
        item.setSizeHint(c.sizeHint())
        self.ibl_list.addItem(item)
        self.ibl_list.setItemWidget(item, c)
        return c

    def init_ui(self):
        # set IBLs
        self.ibl_list = QtGui.QListWidget()
        for ibl in api.get_ibls():
            self.add_ibl(title=ibl.get("title"),
                         type=ibl.get("type"),
                         lighting=ibl.get("lighting"),
                         comments=ibl.get("comments"))
        # set projects
        self.project_list = QtGui.QListWidget()
        for p in api.get_projects():
            self.project_list.addItem(QtGui.QListWidgetItem(p))
        self.project_list.setMaximumWidth(180)
        # layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.ibl_list)
        hbox.addWidget(self.project_list)
        w = QtGui.QWidget()
        w.setLayout(hbox)
        self.setCentralWidget(w)
        self.resize(1024, 550)

from PySide import QtGui, QtCore
from ibl_stuff import api


class Preview(QtGui.QGraphicsView):

    def __init__(self, ibl_data, *arg, **kwds):
        super(Preview, self).__init__(*arg, **kwds)
        self.ibl_data = ibl_data
        for x in (self.setHorizontalScrollBarPolicy,
                  self.setVerticalScrollBarPolicy):
            x(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedSize(250, 125)
        self.setScene(QtGui.QGraphicsScene())
        self.init_scene()

    def add_pixmap(self, image):
        pixmap = QtGui.QPixmap(image)
        pixItem = QtGui.QGraphicsPixmapItem(pixmap)
        scn = self.scene()
        scn.addItem(pixItem)
        return pixItem

    def init_scene(self):
        self.ui_pano = self.add_pixmap(self.ibl_data.get("pano"))
        self.ui_sample = self.add_pixmap(self.ibl_data.get("sample"))
        self.ui_sample.setVisible(False)

    def mousePressEvent(self, event):
        super(Preview, self).mousePressEvent(event)
        self.ui_sample.setVisible(not self.ui_sample.isVisible())
        self.ui_pano.setVisible(not self.ui_pano.isVisible())


class Card(QtGui.QWidget):

    labels = ("title", "type", "lighting", "comments")

    def __init__(self, ibl_data):
        super(Card, self).__init__()
        self.ibl_data = ibl_data
        self.init_ui()

    def init_ui(self):
        # create qwidgets
        self.ui_thumb = Preview(self.ibl_data)
        for each in self.labels:
            setattr(self, "ui_" + each, QtGui.QLabel())
            getattr(self, "ui_" + each).setMaximumWidth(450)
        f = self.ui_title.font()
        f.setPointSize(f.pointSize() * 1.5)
        f.setBold(True)
        f.setCapitalization(QtGui.QFont.AllUppercase)
        self.ui_title.setFont(f)
        self.ui_comments.setWordWrap(True)
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

    def update(self, data=None):
        if data:
            self.ibl_data = data
        for x in self.labels:
            d = self.ibl_data.get(x)
            getattr(self, "ui_" + x).setText(d)

    def get(self, arg):
        if not self.ibl_data:
            self.ibl_data = dict()  # init
        return self.ibl_data.get(arg)


class SearchLineEdit(QtGui.QLineEdit):

    def keyReleaseEvent(self, event):
        super(SearchLineEdit, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.setVisible(False)
            self.setText("")


class Explorer(QtGui.QMainWindow):

    def __init__(self, *arg, **kwds):
        super(Explorer, self).__init__(*arg, **kwds)
        title = "IBL Stuff - " + type(self).__name__.replace("_", " ")
        self.setWindowTitle(title)
        self.ibl_cache = dict()
        self.init_ui()

    def keyReleaseEvent(self, event):
        super(Explorer, self).keyReleaseEvent(event)
        if not self.ibl_list.hasFocus():
            return
        k = event.key()
        if k == QtCore.Qt.Key.Key_Escape:
            self.search_ibl.setVisible(False)
            self.search_ibl.setText("")
        elif event.text().lower() in "abcdefghijklmnopqrstuvwxyz1234567890" and \
                k not in (QtCore.Qt.Key.Key_Left,
                          QtCore.Qt.Key.Key_Right,
                          QtCore.Qt.Key.Key_Up,
                          QtCore.Qt.Key.Key_Down,
                          QtCore.Qt.Key.Key_Return,
                          QtCore.Qt.Key.Key_Enter,
                          16777221, 16777248):  # last 2 are triggered by maya!
            self.search_ibl.setVisible(True)
            self.search_ibl.setFocus()
            self.search_ibl.setText(event.text())

    def add_ibl(self, ibl):
        c = Card(ibl)
        item = QtGui.QListWidgetItem()
        item.setSizeHint(c.sizeHint())
        self.ibl_list.addItem(item)
        self.ibl_list.setItemWidget(item, c)
        self.ibl_cache[ibl.get("title")] = item

    def filter_ibl_list(self, word):
        results = [x.get("title") for x in api.search_ibl(word)]
        for k, v in self.ibl_cache.iteritems():
            v.setHidden(k not in results)

    def init_ui(self):
        # set IBLs
        self.search_ibl = SearchLineEdit()
        self.search_ibl.textChanged.connect(self.filter_ibl_list)
        self.search_ibl.setVisible(False)
        self.ibl_list = QtGui.QListWidget()
        for ibl in api.get_ibls():
            self.add_ibl(ibl)
        # set projects
        self.project_list = QtGui.QListWidget()
        for p in api.get_projects():
            self.project_list.addItem(QtGui.QListWidgetItem(p))
        self.project_list.setMaximumWidth(180)
        # layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.search_ibl)
        vbox.addWidget(self.ibl_list)
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.project_list)
        w = QtGui.QWidget()
        w.setLayout(hbox)
        self.setCentralWidget(w)
        self.resize(900, 550)

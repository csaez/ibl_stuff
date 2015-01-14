from PySide import QtGui, QtCore
from ibl_stuff import api


class DetailedView(QtGui.QDialog):

    LABELS = ("title", "type", "lighting", "location", "tags", "author",
              "date", "comments")

    def __init__(self, ibl_data=None, *arg, **kwds):
        super(DetailedView, self).__init__(*arg, **kwds)
        self.ibl_data = ibl_data or dict()
        self.setWindowTitle("IBL Stuff - " + type(self).__name__)
        self.init_ui()

    def init_ui(self):
        self.ui_preview = Preview()
        italic = QtGui.QFont()
        italic.setItalic(True)
        form = QtGui.QFormLayout()
        for l in self.LABELS:
            label = QtGui.QLabel(l.capitalize() + ":")
            label.setFont(italic)
            w = (QtGui.QLineEdit, QtGui.QPlainTextEdit)[int(l == "comments")]
            setattr(self, l, w())
            form.addRow(label, getattr(self, l))
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.ui_preview)
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(form)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.resize(350, 500)

    def update_ui(self, ibl_data=None):
        if ibl_data is not None:
            self.ibl_data = ibl_data
        self.ui_preview.update_ui(self.ibl_data)
        for l in self.LABELS:
            text = self.ibl_data.get(l, str())
            if not isinstance(text, basestring):
                text = ", ".join(text)
            method = ("setText", "setPlainText")[int(l == "comments")]
            getattr(getattr(self, l), method)(text)


class Preview(QtGui.QGraphicsView):

    def __init__(self, ibl_data=None, *arg, **kwds):
        super(Preview, self).__init__(*arg, **kwds)
        self.ibl_data = ibl_data or dict()
        for x in (self.setHorizontalScrollBarPolicy,
                  self.setVerticalScrollBarPolicy):
            x(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedSize(250, 125)
        self.setScene(QtGui.QGraphicsScene())
        self.init_scene()

    def init_scene(self):
        self.ui_pano = self.add_pixmap(self.ibl_data.get("pano"))
        self.ui_sample = self.add_pixmap(self.ibl_data.get("sample"))
        self.ui_sample.setVisible(False)

    def update_ui(self, ibl_data=None):
        if ibl_data is not None:
            self.ibl_data = ibl_data
        self.ui_pano.setPixmap(QtGui.QPixmap(self.ibl_data.get("pano")))
        self.ui_sample.setPixmap(QtGui.QPixmap(self.ibl_data.get("sample")))

    def add_pixmap(self, image):
        pixmapItem = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(image))
        self.scene().addItem(pixmapItem)
        return pixmapItem

    def mousePressEvent(self, event):
        super(Preview, self).mousePressEvent(event)
        self.ui_sample.setVisible(not self.ui_sample.isVisible())
        self.ui_pano.setVisible(not self.ui_pano.isVisible())


class Card(QtGui.QWidget):

    LABELS = ("title", "type", "lighting", "comments")

    def __init__(self, ibl_data):
        super(Card, self).__init__()
        self.ibl_data = ibl_data
        self.init_ui()

    def init_ui(self):
        # create qwidgets
        self.ui_preview = Preview(self.ibl_data)
        for each in self.LABELS:
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
        hbox.addWidget(self.ui_preview)
        hbox.addLayout(label_vbox)
        self.setLayout(hbox)
        self.update_ui()

    def update_ui(self, data=None):
        if data:
            self.ibl_data = data
        for x in self.LABELS:
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
            self.setHidden(True)
            self.setText("")


class Explorer(QtGui.QMainWindow):

    def __init__(self, *arg, **kwds):
        super(Explorer, self).__init__(*arg, **kwds)
        title = "IBL Stuff - " + type(self).__name__
        self.setWindowTitle(title)
        self.ui_dview = DetailedView(parent=self)
        self.ibl_cache = dict()
        self.init_ui()

    def init_ui(self):
        # set IBLs
        self.ui_search = SearchLineEdit()
        self.ui_search.textChanged.connect(self.filter_ibls)
        self.ui_search.setHidden(True)
        self.ui_ibls = QtGui.QListWidget()
        for ibl in api.get_ibls():
            self.add_ibl(ibl)
        # set projects
        self.ui_project = QtGui.QListWidget()
        for p in api.get_projects():
            self.ui_project.addItem(QtGui.QListWidgetItem(p))
        self.ui_project.setMaximumWidth(180)
        # layout
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.ui_search)
        vbox.addWidget(self.ui_ibls)
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.ui_project)
        cw = QtGui.QWidget()
        cw.setLayout(hbox)
        self.setCentralWidget(cw)
        self.resize(900, 550)
        # connect signals
        self.ui_ibls.itemDoubleClicked.connect(self.open_dview)

    def add_ibl(self, ibl):
        c = Card(ibl)
        item = QtGui.QListWidgetItem()
        item.setSizeHint(c.sizeHint())
        self.ui_ibls.addItem(item)
        self.ui_ibls.setItemWidget(item, c)
        self.ibl_cache[ibl.get("title")] = item

    def filter_ibls(self, word):
        results = [x.get("title") for x in api.search_ibl(word)]
        for k, v in self.ibl_cache.iteritems():
            v.setHidden(k not in results)

    def open_dview(self, item):
        for k, v in self.ibl_cache.iteritems():
            if item is not v:
                continue
            ibl = api.get_ibl(k)
            self.ui_dview.update_ui(ibl)
            self.ui_dview.exec_()
            return

    def keyReleaseEvent(self, event):
        super(Explorer, self).keyReleaseEvent(event)
        if not self.ui_ibls.hasFocus():
            return
        k = event.key()
        if k == QtCore.Qt.Key.Key_Escape:
            self.ui_search.setHidden(True)
            self.ui_search.setText("")
        elif event.text().lower() in "abcdefghijklmnopqrstuvwxyz1234567890" and \
                k not in (QtCore.Qt.Key.Key_Left,
                          QtCore.Qt.Key.Key_Right,
                          QtCore.Qt.Key.Key_Up,
                          QtCore.Qt.Key.Key_Down,
                          QtCore.Qt.Key.Key_Return,
                          QtCore.Qt.Key.Key_Enter,
                          16777221, 16777248):  # last 2 are triggered by maya!
            self.ui_search.setHidden(False)
            self.ui_search.setFocus()
            self.ui_search.setText(event.text())

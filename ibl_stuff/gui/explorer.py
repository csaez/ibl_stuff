from PySide import QtGui, QtCore

from ibl_stuff import api
from ibl_stuff.gui.preview import Preview
from ibl_stuff.gui.detailed_view import DetailedView


class Card(QtGui.QWidget):

    LABELS = ("title", "type", "lighting", "comments")

    def __init__(self, ibl):
        super(Card, self).__init__()
        self.ibl = ibl
        self.init_ui()

    def init_ui(self):
        # create qwidgets
        self.ui_preview = Preview(self.ibl)
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
            self.ibl = data
        for x in self.LABELS:
            d = self.ibl.get(x)
            getattr(self, "ui_" + x).setText(d)

    def get(self, arg):
        if not self.ibl:
            self.ibl = dict()  # init
        return self.ibl.get(arg)


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
        self.ibl_cache = dict()
        self.init_ui()

    def init_ui(self):
        # set IBLs
        self.ui_search = SearchLineEdit()
        self.ui_search.setHidden(True)
        self.ui_ibls = QtGui.QListWidget()
        # set projects
        self.ui_project = QtGui.QListWidget()
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
        self.ui_search.textChanged.connect(self.filter_ibls)
        self.ui_ibls.itemDoubleClicked.connect(self.open_dview)
        self.ui_project.itemClicked.connect(self.filter_by_project)
        # fill gui
        self.reload()

    def reload(self):
        # add ibls
        self.ui_ibls.clear()
        for ibl in api.get_ibls():
            self.add_ibl(ibl)
        # add projects
        projects = api.get_projects()
        self.ui_project.clear()
        for p in projects:
            self.ui_project.addItem(QtGui.QListWidgetItem(p))

    def update_projects(self):
        projects = set(api.get_projects())
        items = set([self.ui_project.item(i).text()
                     for i in range(self.ui_project.count())])
        to_remove = items - projects
        to_add = projects - items
        # remove unused projects
        for prj in to_remove:
            self.remove_item(prj)
        # add new items
        for prj in to_add:
            self.ui_project.addItem(QtGui.QListWidgetItem(prj))

    def remove_item(self, item_text):
        for i in range(self.ui_project.count()):
            item = self.ui_project.item(i)
            if not item:
                continue
            if item.text() == item_text:
                self.ui_project.takeItem(i)
                return True
        return False

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

    def filter_by_project(self):
        prj = self.ui_project.item(self.ui_project.currentRow() or 0)
        if not prj:
            return
        prj = prj.text()
        if prj == "None":
            prj = None
        results = [x.get("title") for x in api.get_ibls(prj)]
        for k, v in self.ibl_cache.iteritems():
            v.setHidden(k not in results)

    def open_dview(self, item):
        for k, v in self.ibl_cache.iteritems():
            if item is not v:
                continue
            ibl = api.get_ibl(k)
            dview = DetailedView(ibl, parent=self)
            if dview.exec_():
                # update card
                item = self.ibl_cache.get(ibl.get("title"))
                card = self.ui_ibls.itemWidget(item)
                card.update_ui(ibl)
                self.update_projects()
                self.filter_by_project()
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

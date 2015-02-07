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


class NewIBL(QtGui.QInputDialog):

    @classmethod
    def get_ibl(cls, *arg, **kwds):
        ob = cls(*arg, **kwds)
        ok = ob.exec_()
        if ok:
            ibl = api.get_ibl(ob.get_text())
            return ibl
        return None

    def __init__(self, *arg, **kwds):
        super(NewIBL, self).__init__(*arg, **kwds)
        self.setWindowTitle("New IBL")
        self.setLabelText("IBL title")
        self.ibl_titles = [x.get("title").lower() for x in api.get_ibls()]
        self.textValueChanged.connect(self.validate)
        self.ibl = None

    def is_valid(self):
        text = self.get_text()
        if text:
            len_text = bool(len(text))
            return text.lower() not in self.ibl_titles and len_text

    def validate(self, text):
        btn = self.get_button("OK")
        if btn:
            btn.setEnabled(self.is_valid())

    def get_button(self, text):
        for child in self.children():
            if not isinstance(child, QtGui.QDialogButtonBox):
                continue
            for btn in child.children():
                if isinstance(btn, QtGui.QPushButton) and text in btn.text():
                    return btn
        return None

    def get_text(self):
        for child in self.children():
            if not isinstance(child, QtGui.QLineEdit):
                continue
            return child.text()
        return None

    def accept(self, *arg, **kwds):
        if self.is_valid():
            self.ibl = api.new_ibl(self.get_text())
            super(NewIBL, self).accept(*arg, **kwds)


class Explorer(QtGui.QMainWindow):

    def __init__(self, *arg, **kwds):
        super(Explorer, self).__init__(*arg, **kwds)
        title = "IBL Stuff - " + type(self).__name__
        self.setWindowTitle(title)
        self.ibl_cache = dict()
        self.init_ui()

    def init_ui(self):
        # set search field
        self.ui_search = SearchLineEdit()
        self.ui_search.setHidden(True)
        # set IBLs
        self.ui_ibls = QtGui.QListWidget()
        # set ibl context menu
        self.ui_ibl_menu = QtGui.QMenu(self)
        menu_items = (
            "Send to Maya",
            "View/Edit Details",
            "Create Empty",
            "Remove",
            "Import",
            "Export",
        )
        for action in menu_items:
            if action in ("Create Empty", "Import"):
                self.ui_ibl_menu.addSeparator()
            self.ui_ibl_menu.addAction(action)
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
        self.ui_ibl_menu.triggered.connect(self.iblActionTriggered)
        self.ui_ibls.contextMenuEvent = self.iblContextMenu
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
        return item

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
        ibl = self.get_ibl_by_card(item)
        if not ibl:
            return
        dview = DetailedView(ibl, parent=self)
        if dview.exec_():
            # update card
            item = self.ibl_cache.get(ibl.get("title"))
            card = self.ui_ibls.itemWidget(item)
            card.update_ui(ibl)
            self.update_projects()
            self.filter_by_project()

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

    def iblContextMenu(self, event):
        self.ui_ibl_menu.move(event.globalPos())
        enabled = ("View/Edit Details", "Create Empty", "Remove")
        for x in self.ui_ibl_menu.children():
            x.setEnabled(x.text() in enabled)
        self.ui_ibl_menu.exec_()

    def iblActionTriggered(self, action):
        item = self.ui_ibls.item(self.ui_ibls.currentRow())
        actions = {
            "View/Edit Details": lambda x=item: self.open_dview(x),
            "Create Empty": self.new_ibl,
            "Remove": lambda x=item: self.remove_ibl(x)
        }
        actions.get(action.text(), lambda: None)()

    def new_ibl(self):
        ibl = NewIBL.get_ibl(parent=self)
        if ibl:
            item = self.add_ibl(ibl)
            self.open_dview(item)

    def remove_ibl(self, item):
        ibl = self.get_ibl_by_card(item)
        if not ibl:
            return
        ok = QtGui.QMessageBox.question(
            self,
            "IBL Stuff",
            "Are you sure you want to delete the selected lightrig?",
            buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if ok != QtGui.QMessageBox.Cancel:
            api.remove_ibl(ibl.get("title"))
            self.ui_ibls.takeItem(self.ui_ibls.currentRow())
            self.update_projects()

    def get_ibl_by_card(self, item):
        for k, v in self.ibl_cache.iteritems():
            if item is v:
                return api.get_ibl(k)
        return None

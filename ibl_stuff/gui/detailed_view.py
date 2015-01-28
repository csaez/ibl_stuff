from PySide import QtGui, QtCore
from ibl_stuff import api
from ibl_stuff.gui.preview import Preview


class DetailedView(QtGui.QDialog):

    LABELS = ("title", "type", "lighting", "projects",
              "location", "tags", "author", "date", "comments")

    def __init__(self, ibl=None, *arg, **kwds):
        super(DetailedView, self).__init__(*arg, **kwds)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ibl = ibl or dict()
        self.setWindowTitle("IBL Stuff - " + type(self).__name__)
        self.init_ui()
        if len(self.ibl):
            self.update_ui()

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
        # buttons
        buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        vbox.addWidget(buttonBox)
        # set and resize
        self.setLayout(vbox)
        self.resize(350, 500)

    def update_ui(self, ibl=None):
        if ibl is not None:
            self.ibl = ibl
        self.ui_preview.update_ui(self.ibl)
        for l in self.LABELS:
            text = self.ibl.get(l, str())
            if not isinstance(text, basestring):
                text = ", ".join(text)
            method = ("setText", "setPlainText")[int(l == "comments")]
            getattr(getattr(self, l), method)(text)

    def update_ibl(self):
        for l in self.LABELS:
            get_text = {
                QtGui.QPlainTextEdit: lambda x: x.toPlainText(),
                QtGui.QLineEdit: lambda x: x.text(),
            }
            label = getattr(self, l)
            text = get_text.get(type(label))(label)
            if l in ("tags", "projects"):
                text = text.split(", ")
            self.ibl[l] = text
        api.save_ibl(self.ibl)

    def accept(self):
        self.update_ibl()
        super(DetailedView, self).accept()

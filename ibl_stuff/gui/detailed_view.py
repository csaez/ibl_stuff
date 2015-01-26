from PySide import QtGui, QtCore
from ibl_stuff.gui.preview import Preview


class DetailedView(QtGui.QDialog):

    LABELS = ("title", "type", "lighting", "location", "tags", "author",
              "date", "comments")

    def __init__(self, ibl_data=None, *arg, **kwds):
        super(DetailedView, self).__init__(*arg, **kwds)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ibl_data = ibl_data or dict()
        self.setWindowTitle("IBL Stuff - " + type(self).__name__)
        self.init_ui()
        if len(self.ibl_data):
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

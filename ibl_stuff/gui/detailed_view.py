from PySide import QtGui, QtCore
from ibl_stuff import api
from ibl_stuff.gui.preview import Preview


class CompleterLineEdit(QtGui.QLineEdit):

    def text_changed(self):
        text = self.text()
        all_text = unicode(text)
        text = all_text[:self.cursorPosition()]
        prefix = text.split(",")[-1].strip()

        text_tags = []
        for t in all_text.split(","):
            t1 = unicode(t).strip()
            if t1 != "":
                text_tags.append(t)
        text_tags = list(set(text_tags))

        return text_tags, prefix

    def complete_text(self, text):
        cursor_pos = self.cursorPosition()
        before_text = unicode(self.text())[:cursor_pos]
        after_text = unicode(self.text())[cursor_pos:]
        prefix_len = len(before_text.split(",")[-1].strip())
        self.setText("%s%s, %s" % (before_text[:cursor_pos - prefix_len], text,
                                   after_text))
        self.setCursorPosition(cursor_pos - prefix_len + len(text) + 2)


class TagsCompleter(QtGui.QCompleter):

    def __init__(self, all_tags, parent):
        super(TagsCompleter, self).__init__(all_tags, parent)
        self.all_tags = set(all_tags)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

    def update(self, _):
        sender = self.sender()
        text_tags, completion_prefix = sender.text_changed()
        tags = list(self.all_tags.difference(text_tags))
        model = QtGui.QStringListModel(tags, self)
        self.setModel(model)

        self.setCompletionPrefix(completion_prefix)
        if completion_prefix.strip() != "":
            self.complete()


class DetailedView(QtGui.QDialog):

    LABELS = ("type", "lighting", "tags", "projects", "location", "author",
              "date", "comments")

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
        for label in self.LABELS:
            ui_label = QtGui.QLabel(label.capitalize() + ":")
            ui_label.setFont(italic)
            widgets = {"comments": QtGui.QPlainTextEdit,
                       "projects": CompleterLineEdit,
                       "tags": CompleterLineEdit}.get(label, QtGui.QLineEdit)
            setattr(self, "ui_" + label, widgets())
            ui_edit = getattr(self, "ui_" + label)
            form.addRow(ui_label, ui_edit)
            # autocomplete
            if label in ("projects", "tags"):
                c = TagsCompleter(getattr(api, "get_" + label)(), self)
                ui_edit.textChanged.connect(c.update)
                c.activated.connect(ui_edit.complete_text)
                c.setWidget(ui_edit)
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
        self.setWindowTitle("IBL Stuff - " + self.ibl.get("title"))
        for label in self.LABELS:
            text = self.ibl.get(label, str())
            if not isinstance(text, basestring):
                text = ", ".join(text)
            widget = getattr(self, "ui_" + label)
            self._set_text(widget, text)

    def update_ibl(self):
        for label in self.LABELS:
            ui_label = getattr(self, "ui_" + label)
            text = self._get_text(ui_label)
            if label in ("tags", "projects"):
                text = text.split(", ")
                text = [x for x in text if x]
            self.ibl[label] = text
        api.save(self.ibl)

    def _get_text(self, widget):
        return {
            QtGui.QPlainTextEdit: lambda x=widget: x.toPlainText(),
            QtGui.QLineEdit: lambda x=widget: x.text(),
        }.get(type(widget), lambda x=widget: x.text())()

    def _set_text(self, widget, text):
        return {
            QtGui.QPlainTextEdit: lambda t, x=widget: x.setPlainText(t),
            QtGui.QLineEdit: lambda t, x=widget: x.setText(t),
        }.get(type(widget), lambda t, x=widget: x.setText(t))(text)

    def accept(self):
        self.update_ibl()
        super(DetailedView, self).accept()

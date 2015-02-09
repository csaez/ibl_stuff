from PySide import QtGui


def get_parent():
    parent = QtGui.QApplication.activeWindow()
    if parent is None:
        return None
    _ = parent.parent()
    while _:
        parent = _
        _ = parent.parent()
    return parent


def find_instance(parent, qt_class):
    for child in parent.children():
        if isinstance(child, qt_class):
            return child
    return None

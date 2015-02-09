import sys
from nose import with_setup
from PySide import QtGui

from ibl_stuff.libs import qt_helpers

PARENT = None


class Foo(QtGui.QDialog):
    pass


class Bar():
    pass


def setup_qt():
    global PARENT
    try:
        QtGui.QApplication(sys.argv)
        PARENT = QtGui.QMainWindow()
        Foo(PARENT)
    except:
        pass


def teardown_qt():
    pass


def test_get_parent_empty():
    assert qt_helpers.get_parent() is None


@with_setup(setup_qt, teardown_qt)
def test_find_instance_success():
    assert qt_helpers.find_instance(PARENT, Foo) is not None


@with_setup(setup_qt, teardown_qt)
def test_find_instance_fail():
    assert qt_helpers.find_instance(PARENT, Bar) is None

import sys

import unittest
from PySide import QtGui
from ibl_stuff.libs import qt_helpers


class Foo(QtGui.QDialog):
    pass


class Bar():
    pass


class SimpleTest(unittest.TestCase):

    def test_get_parent_empty(self):
        assert qt_helpers.get_parent() is None


class TestQt(unittest.TestCase):
    PARENT = None

    def setUp(self):
        try:
            QtGui.QApplication(sys.argv)
        except RuntimeError:
            pass
        self.PARENT = QtGui.QMainWindow()
        Foo(self.PARENT)

    def tearDown(self):
        self.PARENT = None

    def test_find_instance_success(self):
        assert qt_helpers.find_instance(self.PARENT, Foo) is not None

    def test_find_instance_fail(self):
        assert qt_helpers.find_instance(self.PARENT, Bar) is None

if __name__ == "__main__":
    unittest.main()

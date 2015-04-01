import os

import shutil
import unittest
from PySide.QtCore import QSettings

from ibl_stuff.libs import base as libs


LIBRARY = libs.get_library()
ENV_LIBRARY = os.environ.get("IBL_LIBRARY")


class SimpleTests(unittest.TestCase):

    def test_clear_cache(self):
        self.assertTrue(libs.clear_cache())

    def test_save_fail(self):
        self.assertFalse(libs.save_ibl("unmatched_title"))

    def test_load_fail(self):
        self.assertFalse(libs.load_ibl("unmatched_title"))


class TestLibrary(unittest.TestCase):

    def setUp(self):
        _library = os.path.join(os.path.expanduser("~"), "test_library")
        if os.path.exists(_library):
            shutil.rmtree(_library)
        if ENV_LIBRARY:
            del os.environ["IBL_LIBRARY"]
        libs.set_library(_library)
        for i, prj in enumerate(["foo", "bar", "baz"]):
            x = libs.new_ibl("test%d" % i)
            x["projects"] = [prj]
            x["tags"] = [prj]

    def tearDown(self):
        _library = os.path.join(os.path.expanduser("~"), "test_library")
        shutil.rmtree(_library)
        if ENV_LIBRARY:
            os.environ["IBL_LIBRARY"] = ENV_LIBRARY
        libs.set_library(LIBRARY)

    def test_get_library(self):
        os.environ["IBL_LIBRARY"] = "test"
        self.assertEqual(libs.get_library(), "test")

        del os.environ["IBL_LIBRARY"]
        libs.set_library("test")
        self.assertEqual(libs.get_library(), "test")

        QSettings("csaez", "ibl_stuff").clear()
        self.assertEqual(libs.get_library(),
                         os.path.join(os.path.expanduser("~"), "ibl_stuff"))

    def test_get_projects(self):
        prjs = ["bar", "baz", "foo"]
        for prj in libs.get_projects():
            self.assertIn(prj, prjs)
        self.assertEqual(sorted(libs.get_projects()), prjs)

    def test_search_ibl(self):
        for i, prj in enumerate(("foo", "bar", "baz")):
            self.assertEqual(len(libs.search_ibl(prj)), 1)
            self.assertEqual(libs.search_ibl(prj)[0].get("title"),
                             "test%d" % i)

    def test_get_ibl(self):
        for i, prj in enumerate(("foo", "bar", "baz")):
            self.assertEqual(libs.get_ibl("test%d" % i)["projects"], [prj])
        self.assertIsNone(libs.get_ibl("foo"))
        libs.clear_cache()
        self.assertIsNotNone(libs.get_ibl("test0"))

    def test_save_success(self):
        for i in range(3):
            self.assertTrue(libs.save_ibl("test%d" % i))

    def test_load_success(self):
        for i in range(3):
            self.assertTrue(libs.load_ibl("test%d" % i))

    def test_remove_ibl(self):
        self.assertFalse(libs.remove_ibl("foo"))
        for i in range(3):
            self.assertTrue(libs.remove_ibl("test%d" % i))

    def test_get_tags(self):
        self.assertEqual(sorted(libs.get_tags()), ["bar", "baz", "foo"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

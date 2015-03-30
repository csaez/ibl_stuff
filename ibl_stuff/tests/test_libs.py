import os

import shutil
import unittest
from PySide.QtCore import QSettings
from ibl_stuff.libs import base as libs


LIBRARY = libs.get_library()
ENV_LIBRARY = os.environ.get("IBL_LIBRARY")


class SimpleTests(unittest.TestCase):

    def test_clear_cache(self):
        assert libs.clear_cache()

    def test_save_fail(self):
        assert not libs.save_ibl("unmatched_title")

    def test_load_fail(self):
        assert not libs.load_ibl("unmatched_title")


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
        assert libs.get_library() == "test"

        del os.environ["IBL_LIBRARY"]
        libs.set_library("test")
        assert libs.get_library() == "test"

        QSettings("csaez", "ibl_stuff").clear()
        assert libs.get_library() == os.path.join(
            os.path.expanduser("~"), "ibl_stuff")

    def test_get_projects(self):
        prjs = ["bar", "baz", "foo"]
        for prj in libs.get_projects():
            assert prj in prjs
        assert sorted(libs.get_projects()) == prjs

    def test_search_ibl(self):
        for i, prj in enumerate(("foo", "bar", "baz")):
            assert len(libs.search_ibl(prj)) == 1
            assert libs.search_ibl(prj)[0].get("title") == "test%d" % i

    def test_get_ibl(self):
        for i, prj in enumerate(("foo", "bar", "baz")):
            assert libs.get_ibl("test%d" % i)["projects"] == [prj]
        assert libs.get_ibl("foo") is None
        libs.clear_cache()
        assert libs.get_ibl("test0") is not None

    def test_save_success(self):
        for i in range(3):
            assert libs.save_ibl("test%d" % i)

    def test_load_success(self):
        for i in range(3):
            assert libs.load_ibl("test%d" % i)

    def test_remove_ibl(self):
        assert not libs.remove_ibl("foo")
        for i in range(3):
            assert libs.remove_ibl("test%d" % i)

    def test_get_tags(self):
        assert sorted(libs.get_tags()) == ["bar", "baz", "foo"]

if __name__ == "__main__":
    unittest.main(verbosity=2)

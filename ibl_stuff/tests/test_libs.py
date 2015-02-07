import os
import shutil
from nose import with_setup
from PySide.QtCore import QSettings
from ibl_stuff import libs

LIBRARY = libs.get_library()
ENV_LIBRARY = os.environ.get("IBL_LIBRARY")


def test_clear_cache():
    assert libs.clear_cache()


def setup_library():
    _library = os.path.join(os.path.expanduser("~"), "test_library")
    if os.path.exists(_library):
        shutil.rmtree(_library)
    del os.environ["IBL_LIBRARY"]
    libs.set_library(_library)
    for i, prj in enumerate(["foo", "bar", "baz"]):
        x = libs.new_ibl("test%d" % i)
        x["projects"] = [prj]
        x["tags"] = [prj]


def teardown_library():
    _library = libs.get_library()
    shutil.rmtree(_library)
    libs.set_library(LIBRARY)
    if ENV_LIBRARY:
        os.environ["IBL_LIBRARY"] = ENV_LIBRARY


@with_setup(setup_library, teardown_library)
def test_get_library():
    os.environ["IBL_LIBRARY"] = "test"
    assert libs.get_library() == "test"

    del os.environ["IBL_LIBRARY"]
    libs.set_library("test")
    assert libs.get_library() == "test"

    QSettings("csaez", "ibl_stuff").clear()
    assert libs.get_library() == os.path.join(
        os.path.expanduser("~"), "ibl_stuff")


@with_setup(setup_library, teardown_library)
def test_get_projects():
    prjs = ["bar", "baz", "foo"]
    for prj in libs.get_projects():
        assert prj in prjs
    assert sorted(libs.get_projects()) == prjs


@with_setup(setup_library, teardown_library)
def test_search_ibl():
    for i, prj in enumerate(("foo", "bar", "baz")):
        assert len(libs.search_ibl(prj)) == 1
        assert libs.search_ibl(prj)[0].get("title") == "test%d" % i


@with_setup(setup_library, teardown_library)
def test_get_ibl():
    for i, prj in enumerate(("foo", "bar", "baz")):
        assert libs.get_ibl("test%d" % i)["projects"] == [prj]
    assert libs.get_ibl("foo") is None


@with_setup(setup_library, teardown_library)
def test_remove_ibl():
    assert not libs.remove_ibl("foo")
    for i in range(3):
        assert libs.remove_ibl("test%d" % i)


@with_setup(setup_library, teardown_library)
def test_get_tags():
    assert sorted(libs.get_tags()) == ["bar", "baz", "foo"]

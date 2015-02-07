import os
from ibl_stuff.libs import ibl

FILEPATH = os.path.join(os.path.expanduser("~"), "temp.json")
BASE_KEYS = ("title", "type", "lighting", "location", "tags", "projects",
             "author", "date", "comments", "pano", "sample")


def test_ibl():
    for k in ibl.IBL().keys():
        assert k in BASE_KEYS


def test_normalize_path():
    assert ibl.normalize_path("D/E/F/", "A/B/C/") == "A/B/C/D/E/F"
    assert ibl.normalize_path("../../A", "B/C/") == "A"


def test_ibl_import_data_invalid_file():
    x = ibl.IBL()
    assert not x.import_data("/path/to/invalid/file.json")


def test_ibl_import_data():
    ibl.IBL().export_data(FILEPATH)
    assert ibl.IBL().import_data(FILEPATH)


def test_ibl_export_data():
    if os.path.exists(FILEPATH):
        os.remove(FILEPATH)
    ibl.IBL().export_data(FILEPATH)
    assert os.path.exists(FILEPATH)


def test_ibl_save():
    x = ibl.IBL()
    assert not x.save()
    x.filepath = FILEPATH
    assert x.save()


def test_ibl_from_data():
    ibl.IBL().export_data(FILEPATH)
    assert ibl.IBL.from_data(FILEPATH) is not None

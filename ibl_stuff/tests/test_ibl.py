import os

import unittest
from ibl_stuff.libs import ibl


FILEPATH = os.path.join(os.path.expanduser("~"), "temp.json")
BASE_KEYS = ("title", "type", "lighting", "location", "tags", "projects",
             "author", "date", "comments", "pano", "sample")


class TestIBL(unittest.TestCase):

    def test_init(self):
        for k in ibl.IBL().keys():
            self.assertIn(k, BASE_KEYS)

    def test_normalize_path(self):
        self.assertEqual(ibl.normalize_path("D/E/F/", "A/B/C/"), "A/B/C/D/E/F")
        self.assertEqual(ibl.normalize_path("../../A", "B/C/"), "A")

    def test_ibl_import_data_invalid_file(self):
        x = ibl.IBL()
        self.assertFalse(x.import_data("/path/to/invalid/file.json"))

    def test_ibl_import_data(self):
        ibl.IBL().export_data(FILEPATH)
        self.assertTrue(ibl.IBL().import_data(FILEPATH))

    def test_ibl_export_data(self):
        if os.path.exists(FILEPATH):
            os.remove(FILEPATH)
        ibl.IBL().export_data(FILEPATH)
        self.assertTrue(os.path.exists(FILEPATH))

    def test_ibl_save(self):
        x = ibl.IBL()
        self.assertFalse(x.save())
        x.filepath = FILEPATH
        self.assertTrue(x.save())

    def test_ibl_from_data(self):
        ibl.IBL().export_data(FILEPATH)
        self.assertIsNotNone(ibl.IBL.from_data(FILEPATH))

if __name__ == "__main__":
    unittest.main()

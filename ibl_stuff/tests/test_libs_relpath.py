import unittest
from ibl_stuff.libs import relpath


class PathTests(unittest.TestCase):

    def test_pathsplit(self):
        self.assertEqual(relpath.pathsplit("A/B/C", ["D", "E"]),
                         ["A", "B", "C", "D", "E"])
        self.assertEqual(relpath.pathsplit("A/B/C"), ["A", "B", "C"])

    def test_commonpath(self):
        common, l1, l2 = relpath.commonpath("DEF", "DEFG", ["A", "B", "C"])
        self.assertEqual(common, ["A", "B", "C", "D", "E", "F"])
        self.assertEqual(l1, "")
        self.assertEqual(l2, "G")

    def test(self):
        p1 = "A/B/C"
        p2 = "A/B/C/E"
        self.assertEqual(relpath.relpath(p1, p2), "E")
        self.assertEqual(relpath.relpath(p2, p1), "../")

if __name__ == "__main__":
    unittest.main()

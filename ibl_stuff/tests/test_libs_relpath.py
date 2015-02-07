from ibl_stuff.libs import relpath


def test_pathsplit():
    assert relpath.pathsplit("A/B/C", ["D", "E"]) == ["A", "B", "C", "D", "E"]
    assert relpath.pathsplit("A/B/C") == ["A", "B", "C"]


def test_commonpath():
    common, l1, l2 = relpath.commonpath("DEF", "DEFG", ["A", "B", "C"])
    assert common == ["A", "B", "C", "D", "E", "F"]
    assert l1 == ""
    assert l2 == "G"


def test():
    p1 = "A/B/C"
    p2 = "A/B/C/E"
    relpath.test(p1, p2)
    assert relpath.relpath(p1, p2) == "E"
    relpath.test(p2, p1)
    assert relpath.relpath(p2, p1) == "../"

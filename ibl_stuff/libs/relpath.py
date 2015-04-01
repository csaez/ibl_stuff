import os


def pathsplit(p, rest=[]):
    (h, t) = os.path.split(p)
    if len(h) < 1:
        return [t]+rest
    if len(t) < 1:
        return [h]+rest
    return pathsplit(h, [t]+rest)


def commonpath(l1, l2, common=[]):
    if len(l1) < 1:
        return (common, l1, l2)
    if len(l2) < 1:
        return (common, l1, l2)
    if l1[0] != l2[0]:
        return (common, l1, l2)
    return commonpath(l1[1:], l2[1:], common+[l1[0]])


def relpath(p1, p2):
    (common, l1, l2) = commonpath(pathsplit(p1), pathsplit(p2))
    p = []
    if len(l1) > 0:
        p = ["../" * len(l1)]
    p = p + l2
    return os.path.join(*p)

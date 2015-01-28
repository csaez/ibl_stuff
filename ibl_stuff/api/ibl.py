import os
import json


BASE = {"title": "",
        "type": "",
        "lighting": "",
        "location": "",
        "tags": list(),
        "projects": list(),
        "author": "",
        "date": "",
        "comments": "",
        "pano": "/home/csaez/Works/dev/ibl_stuff/refs/pano.png",
        "sample": "/home/csaez/Works/dev/ibl_stuff/refs/sample.png",
        }


def normalize_path(fp, start="/"):
    if "./" in fp[:3]:  # is relative
        basedir = start if os.path.isdir(start) else os.path.dirname(start)
        fp = os.path.join(basedir, fp)
    return os.path.normpath(fp)


class IBL(dict):

    def __init__(self, *arg, **kwds):
        self.update(BASE)
        super(IBL, self).__init__(*arg, **kwds)

    def export_data(self, filepath):
        # validate filepath
        if not os.path.isfile(filepath):
            return False
        d = self.copy()
        # save paths relatives to json filepath
        for attr in ("pano", "sample"):
            d[attr] = os.path.relpath(d.get(attr), filepath)
        # export as json
        with open(filepath, "w") as fp:
            json.dump(d, fp, indent=4, separators=(",", ": "))
        return True

    def import_data(self, filepath):
        # validate filepath
        if not os.path.isfile(filepath):
            return False
        # import data
        with open(filepath) as fp:
            d = json.load(fp)
        # normalize paths to absolute
        for attr in ("pano", "sample"):
            d[attr] = normalize_path(d[attr], filepath)
        # update and success
        self.update(d)
        return True

    @classmethod
    def from_data(cls, filepath):
        o = cls()
        o.import_data(filepath)
        return o

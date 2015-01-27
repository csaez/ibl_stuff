import json

IBL_PATH = "/home/csaez/Works/dev/ibl_stuff/refs/pano.png"
SAMPLE_PATH = "/home/csaez/Works/dev/ibl_stuff/refs/sample.png"

BASE = {"title": "",
        "type": "",
        "lighting": "",
        "location": "",
        "tags": list(),
        "projects": list(),
        "author": "",
        "date": "",
        "comments": "",
        "pano": IBL_PATH,
        "sample": SAMPLE_PATH,
        }


class IBL(dict):

    def __init__(self, *arg, **kwds):
        self.update(BASE)
        super(IBL, self).__init__(*arg, **kwds)

    def export_data(self, filepath):
        with open(filepath, "w") as fp:
            json.dump(self, fp, indent=4, separators=(",", ": "))

    def import_data(self, filepath):
        with open(filepath) as fp:
            d = json.load(fp)
        self.update(d)

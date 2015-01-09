import json


class IBL_Data(dict):

    _IBL_KEYS = ("thumbnail", "render", "title", "type", "lighting",
                 "location", "tags", "author", "date")

    def __init__(self, *arg, **kwds):
        super(IBL_Data, self).__init__(*arg, **kwds)
        for key in self._IBL_KEYS:
            default_value = str() if key != "tags" else list()
            self.__setitem__(key, default_value)

    def __getattr__(self, attr):
        if attr in self._IBL_KEYS:
            return self.__getitem__(attr)
        return super(self, IBL_Data).__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr in self._IBL_KEYS:
            return self.__setitem__(attr, value)
        return super(self, IBL_Data).__setattr__(attr, value)

    def import_json(self, json_file):
        with open(json_file) as fp:
            d = json.load(fp)
        self.update(d)

    def export_json(self, json_file):
        d = dict([(k, self.get(k)) for k in self._IBL_KEY])
        with open(json_file, "w") as fp:
            json.dump(d, fp)


def _create_ibl(*args, **kwrgs):
    ibl = IBL_Data()
    keys = ("title", "type", "lighting", "location", "tags", "author", "date")
    # check args
    for i, arg in enumerate(args):
        k = keys[i]
        ibl[k] = arg
    # check kwkwrgs
    for k in keys:
        v = kwrgs.get(k)
        if v:
            ibl[k] = v
    return ibl


def get_ibls():
    # placeholder!
    return (
        _create_ibl("Sunny Boat",
                    "Look-dev",
                    "Sunny",
                    "Portree, Isle of Skye, Scotland",
                    ("exterior",
                     "town",
                     "sea",
                     "natural environment",
                     "docks",
                     "sunny",
                     "winter"),
                    "Xuan Prada",
                    "12-Feb-2014"),
        _create_ibl("Darwing Room",
                    "Look-Dev",
                    "Cloudy",
                    "Mieres, Asturias, Spain",
                    ("interior",
                     "industrial",
                     "destroyed",
                     "sunny",
                     "shade",
                     ),
                    "Xuan Prada",
                    "09-Mar-2014"),
        _create_ibl("Pinewood Studios, Stage 02",
                    "Texture checker",
                    "Neutral",
                    "Pinewood Studios, London, UK",
                    ("interior",
                     "artificial",
                     "on-set",
                     "studio",
                     ),
                    "Xuan Prada",
                    "21-Apr-2014"),
        _create_ibl("Millennium Bridge",
                    "Look-Dev",
                    "Cloudy",
                    "City of Westminster, London, UK",
                    ("exterior",
                     "urban",
                     "cloudy",
                     "stormy",
                     ),
                    "Xuan Prada",
                    "17-May-2014"),
        _create_ibl("The Old Man of Storr",
                    "Look-dev",
                    "Cloudy",
                    "Portree, Isle of Skye, Scotland",
                    ("exterior",
                     "natural",
                     "rocks",
                     "cloudy",
                     "stormy",
                     ),
                    "Xuan Prada",
                    "24-Jun-2014"),
        _create_ibl("Studio C",
                    "Model checker",
                    "Neutral",
                    "Computer generated",
                    ("interior",
                     "artificial",
                     "studio",
                     "cg generated",
                     ),
                    "Xuan Prada",
                    "04-Jul-2014"),
        _create_ibl("Mercury Mine",
                    "Look-dev",
                    "Sunny",
                    "Mieres, Asturis, Spain",
                    ("interior",
                     "industrial",
                     "destroyed",
                     "sunny",
                     "shade",
                     ),
                    "Xuan Prada",
                    "17-Aug-2014"),
    )

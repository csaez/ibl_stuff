IBL_PATH = "/home/csaez/Works/dev/ibl_stuff/refs/pano.png"
SAMPLE_PATH = "/home/csaez/Works/dev/ibl_stuff/refs/sample.png"


def get_projects():
    return (
        "Iron Man 4",
        "Fast And Furious 9",
        "Back To The Future IV",
        "Jurassic Park 6",
        "The Gonnies 2",
        "Alice In Wonderland Retrospective",
        "Ghostbusters 5",
        "Planet 52",
        "Ice Age 7",
        "Mad Max 5",
        "The Adderal Diaries",
    )


def get_ibls():
    return ({"title": "Sunny Boat",
             "type": "Look-dev",
             "lighting": "Sunny",
             "location": "Portree, Isle of Skye, Scotland",
             "tags": ("exterior",
                      "town",
                      "sea",
                      "natural environment",
                      "docks",
                      "sunny",
                      "winter"),
             "author": "Xuan Prada",
             "date": "12-Feb-2014",
             "comments": "This IBL was shot for the coat crash sequence.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "Drawing Room",
             "type": "Look-Dev",
             "lighting": "Cloudy",
             "location": "Mieres, Asturias, Spain",
             "tags": ("interior",
                      "industrial",
                      "destroyed",
                      "sunny",
                      "shade",
                      ),
             "author": "Xuan Prada",
             "date": "09-Mar-2014",
             "comments": "To be used for digital doubles in pt_mc_04 seq.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "Pinewood Studios, Stage 02",
             "type": "Texture checker",
             "lighting": "Neutral",
             "location": "Pinewood Studios, London, UK",
             "tags": ("interior",
                      "artificial",
                      "on-set",
                      "studio",
                      ),
             "author": "Xuan Prada",
             "date": "21-Apr-2014",
             "comments": "Delorean textures need to be approved using this.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "Millennium Bridge",
             "type": "Look-Dev",
             "lighting": "Cloudy",
             "location": "City of Westminster, London, UK",
             "tags": ("exterior",
                      "urban",
                      "cloudy",
                      "stormy",
                      ),
             "author": "Xuan Prada",
             "date": "17-May-2014",
             "comments": "This IBL is for look-deving the digital building " +
                         "for the opening sequence.\n" +
                         "Important: Forgot to shoot Macbeth charts, use " +
                         "grey ball for color grading.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "The Old Man of Storr",
             "type": "Look-dev",
             "lighting": "Cloudy",
             "location": "Portree, Isle of Skye, Scotland",
             "tags": ("exterior",
                      "natural",
                      "rocks",
                      "cloudy",
                      "stormy",
                      ),
             "author": "Xuan Prada",
             "date": "24-Jun-2014",
             "comments": "To be used for CG cars in jm_pr_02 sequence.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "Studio C",
             "type": "Model checker",
             "lighting": "Neutral",
             "location": "Computer generated",
             "tags": ("interior",
                      "artificial",
                      "studio",
                      "cg generated",
                      ),
             "author": "Xuan Prada",
             "date": "04-Jul-2014",
             "comments": "CG models need to be approved using this IBL.",
             "pano": IBL_PATH,
             "sample": SAMPLE_PATH,
             },
            {"title": "Mercury Mine",
             "type": "Look-dev",
             "lighting": "Sunny",
             "location": "Mieres, Asturis, Spain",
             "tags": ("interior",
                      "industrial",
                      "destroyed",
                      "sunny",
                      "shade",
                      ),
             "author": "Xuan Prada",
             "date": "17-Aug-2014",
             "comments": "To be used for look-deving digital dogs",
             "pano": IBL_PATH,
             "sample":  SAMPLE_PATH,
             },
            )


def search_ibl(word, ibl_subset=None):
    if ibl_subset is None:
        ibl_subset = get_ibls()
    word = word.lower()
    matches = list()
    for ibl in ibl_subset:
        ratio = 0
        for values in ibl.values():
            values = (values, ) if isinstance(values, basestring) else values
            for v in values:
                v = v.lower()
                if word in v:
                    ratio += 1
        if ratio > 0:
            matches.append((ratio, ibl))
        matches.sort(key=lambda x: x[0], reverse=True)
    return zip(*matches)[1]

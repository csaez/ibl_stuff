import os
from ibl_stuff.api.ibl import IBL


def clear_cache():
    global CACHE
    CACHE = {
        "searches": dict(),
        "ibls": dict(),
        "projects": dict(),
    }
    return True


CACHE = dict()
clear_cache()


def get_library():
    library = os.environ.get("IBL_LIBRARY")
    if library is None:
        library = os.path.join(os.path.expanduser("~"), "ibl_stuff")
    if not os.path.exists(library):
        os.makedirs(library)
    return library


def get_projects():
    # check cache
    projects = CACHE["projects"].keys()
    if len(projects):
        return projects
    # collect from ibls
    ibls = get_ibls()
    projects = dict()
    for ibl in ibls:
        prjs = ibl.get("projects")
        if not prjs:
            continue
        for p in prjs.split(", "):
            k = projects.get(p)
            if not k:
                projects[p] = list()
            projects[p].append(ibl.get("title"))
    # add to cache
    CACHE["projects"].update(projects)
    return projects.keys()


def get_ibls(project=None):
    # get from cache
    if project is None:
        ibls = CACHE["ibls"].values()
    else:
        ibls = [CACHE["ibl"].get(x) for x in CACHE["projects"].get(project)]
        ibls = [x for x in ibls if x is not None]
    if len(ibls):
        return ibls
    # collect from filesystem
    ibls = list()
    for dirpath, _, filenames in os.walk(get_library()):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            ibl = IBL.from_data(os.path.join(dirpath, filename))
            if project in ibl.get("projects") or project is None:
                ibls.append(ibl)
            CACHE["ibls"][ibl.get("title")] = ibl
    # add to cache
    CACHE["projects"][str(project)] = [x.get("title") for x in ibls]
    return ibls


def search_ibl(word, project=None):
    word = word.lower()
    # check if cached
    cached = CACHE["searches"].get(word)
    if cached:
        return cached
    # compute search
    matches = list()
    for ibl in get_ibls(project):
        ratio = 0
        for values in ibl.values():
            values = (values, ) if isinstance(values, basestring) else values
            for v in values:
                ratio += int(word in v.lower())
        if ratio > 0:
            matches.append((ratio, ibl))
        matches.sort(key=lambda x: x[0], reverse=True)
    results = zip(*matches)[1] if len(matches) else list()
    CACHE["searches"][word] = results  # add to cache
    return results


def get_ibl(title):
    # try cache first
    ibl = CACHE["ibls"].get(title)
    if ibl:
        return ibl
    # search
    ibls = search_ibl(title)
    if len(ibls):
        ibl = ibls[0]
        # add to cache
        CACHE["ibls"][ibl.get("title")] = ibl
        return ibl
    return None

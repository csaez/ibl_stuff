import os
import shutil
from PySide.QtCore import QSettings
from ibl_stuff.libs.ibl import IBL


def clear_cache():
    global CACHE
    CACHE = {
        "searches": dict(),
        "ibls": dict(),
        "projects": dict(),
        "tags": list(),
    }
    return True


def get_library():
    library = os.environ.get("IBL_LIBRARY")
    if not library:
        try:
            s = QSettings("csaez", "ibl_stuff")
            library = s.value("library")
        except:
            pass
    if not library:
        library = os.path.join(os.path.expanduser("~"), "ibl_stuff")
        set_library(library)
    if not os.path.exists(library):
        os.makedirs(library)
    return library


def set_library(library_path):
    library_path = os.path.normpath(library_path)
    settings = QSettings("csaez", "ibl_stuff")
    settings.setValue("library", library_path)
    clear_cache()
    return True


def get_projects():
    # check cache
    projects = CACHE["projects"].keys()
    if len(projects) > 1:
        return projects
    # collect from ibls
    ibls = get_ibls()
    projects = dict()
    for ibl in ibls:
        prjs = ibl.get("projects")
        if not prjs:
            continue
        for p in prjs:
            p = p or "None"
            k = projects.get(p)
            if not k:
                projects[p] = list()
            projects[p].append(ibl.get("title"))
    # add to cache
    CACHE["projects"] = projects
    return projects.keys()


def get_ibls(project=None):
    if project is "None":
        project = None
    # get from cache
    if project is None:
        ibls = CACHE["ibls"].values()
    else:
        ibls = [CACHE["ibls"].get(x) for x in CACHE["projects"].get(project)]
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
    if len(ibls) and ibls[0]["title"] == title:
        ibl = ibls[0]
        # add to cache
        CACHE["ibls"][ibl.get("title")] = ibl
        return ibl
    return None


def load_ibl(title):
    ibl = get_ibl(title)
    return load(ibl)


def load(ibl):
    if not ibl:
        return False
    # TODO: implement load function
    print "LOADING", ibl.get("title")
    return True


def new_ibl(title):
    src = os.path.join(os.path.dirname(__file__), "..", "data", "template")
    dst = os.path.join(get_library(), title)
    copy_anything(src, dst)
    data = os.path.join(dst, "metadata.json")
    ibl = IBL.from_data(data)
    ibl["title"] = title
    save(ibl)
    return ibl


def remove_ibl(title):
    ibl = get_ibl(title)
    if not ibl:
        return False
    if ibl.filepath:
        shutil.rmtree(os.path.dirname(ibl.filepath))
    del CACHE["ibls"][title]
    CACHE["searches"] = dict()
    CACHE["projects"] = dict()
    CACHE["tags"] = list()
    return True


def copy_anything(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy(src, dst)


def save_ibl(title):
    ibl = get_ibl(title)
    if ibl:
        return save(ibl)
    return False


def save(ibl):
    ibl.save()
    CACHE["ibls"][ibl.get("title")] = ibl
    # force cache update
    CACHE["projects"] = dict()
    CACHE["tags"] = list()
    CACHE["searches"] = dict()
    return True


def get_tags():
    # check cache
    tags = CACHE["tags"]
    if len(tags):
        return tags
    # collect tags
    tags = list()
    for ibl in get_ibls():
        tags.extend(ibl.get("tags"))
    tags = list(set(tags))
    # update CACHE
    CACHE["tags"] = tags
    # return
    return tags

CACHE = dict()
clear_cache()

import os
from ibl import IBL

CACHE = {"searches": dict(), "ibls": dict()}


def clear_cache():
    global CACHE
    CACHE = {"searches": dict(), "ibls": dict()}
    return True


def get_repo():
    repo = os.path.join(os.path.expanduser("~"), "ibl_stuff")
    if not os.path.exists(repo):
        os.makedirs(repo)
    return repo


def get_projects():
    # check cache
    projects = CACHE["ibls"].keys()
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
            projects[p].append(ibl)
    # add to cache
    CACHE["ibls"].update(projects)
    return projects.keys()


def get_ibls(project=None):
    project = project or "ALL"
    # get from cache
    ibls = CACHE["ibls"].get(project)
    if ibls:
        return ibls
    # collect from filesystem
    ibls = list()
    for dirpath, _, filenames in os.walk(get_repo()):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            x = IBL()
            x.import_data(filepath)
            if project in x.get("projects") or project == "ALL":
                ibls.append(x)
    # add to cache
    CACHE["ibls"][project] = ibls
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
    ibls = search_ibl(title)
    if len(ibls):
        return ibls[0]
    return None

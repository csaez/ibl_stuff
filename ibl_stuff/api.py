from imp import find_module
from importlib import import_module

HOST_MODULES = {
    "maya": "ibl_stuff.libs.maya",
    "nuke": "ibl_stuff.libs.nuke",
    "base": "ibl_stuff.libs.base"
}


def _find(name):
    result = True
    try:
        find_module(name)
    except ImportError:
        result = False
    return result


def _override_globals(host):
    mod = HOST_MODULES.get(host, HOST_MODULES.get("base"))
    module = import_module(mod)
    global_table = globals()
    global_table.update(module.__dict__)


def init_host(host=None):
    if host is not None:  # explicitly defined
        _override_globals(host)
        return
    else:  # lets try to figure out automagically
        hosts = [x for x in HOST_MODULES.keys() if x != "base"]
        for guess in hosts:
            if _find(guess):
                _override_globals(guess)
                return
    _override_globals("base")

init_host()

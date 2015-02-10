from imp import find_module
from importlib import import_module


def _find(name):
    result = True
    try:
        find_module(name)
    except ImportError:
        result = False
    return result


def _override_globals(host):
    host_modules = {
        "maya": "ibl_stuff.libs.maya",
        "nuke": "ibl_stuff.libs.nuke",
    }
    mod = host_modules.get(host, "ibl_stuff.libs.base")
    module = import_module(mod)
    global_table = globals()
    global_table.update(module.__dict__)


def init_host(host=None):
    _override_globals("base")
    if host is not None:  # explicitly defined
        _override_globals(host)
    else:  # lets try to figure out automagically
        for guess in ("maya", "nuke"):
            if _find(guess):
                _override_globals(guess)
                return

init_host()

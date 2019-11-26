from importlib import import_module
from pkgutil import iter_modules

__author__ = "isnanda.muhammadzain@sebangsa.com"


def walk_modules(path):
    """Load a module
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, "__path__"):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + "." + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods
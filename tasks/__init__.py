from invoke import Collection, Task, task

import inspect

# the toplevel commands module
from . import toplevel

# core modules for this project
from .modules import core
from .modules import py
from .modules import git
from .modules import meta
from .modules import project
from .modules import org
from .modules import env
from .modules import update

# then load all of the submodule namespaces
modules = [core, py, git, project, org, env, update, ]

# these helper functions are for automatically listing all of the
# functions defined in the tasks module

def _is_mod_task(mod, func):
    return issubclass(type(func), Task) and inspect.getmodule(func) == mod

def _get_functions(mod):
    """get only the functions that aren't module functions and that
    aren't private (i.e. start with a '_')"""

    return {func.__name__ : func for func in mod.__dict__.values()
            if _is_mod_task(mod, func) }

# add all of the modules to the CLI
ns = Collection()

# get all the functions from the toplevel module, and add them to the
# toplevel collection
for func in _get_functions(toplevel).values():
    ns.add_task(func)



for module in modules:
    ns.add_collection(module)

# then the user defined plugins

try:
    # import all the user defined stuff and override
    from .plugins import PLUGIN_MODULES as plugins

    for module in plugins:
        ns.add_collection(module)

except Exception as e:
    print("Loading plugins failed with error ignoring:")
    print(e)

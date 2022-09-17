
import sys
import importlib
from pathlib import Path


_callbacks = {}
'''
Register callbacks
hook - the name of the hook to register
order - the order in the callback chain it should be called. defaults to 0
'''
def register(hook, order = 0):
    def register_callback(func):
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(func)
        return func

    return register_callback

def event(hook, *args):
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            func(*args)

def filter(hook, value, *args) :
    for order in sorted(_callbacks.get(hook, {})) :
        for func in _callbacks[hook][order] :
            value = func(value, *args)
    return value

def load_module(directory, name) :
    sys.path.insert(0, directory)
    importlib.import_module(name)
    sys.path.pop(0)

def load_directory(directory) :
    for path in directory.rglob("*.py"):
        load_module(directory.as_posix(path), path.stem)

def load_bundled() :
    directory = Path(__file__).parent / "extensions"
    load_directory(directory)


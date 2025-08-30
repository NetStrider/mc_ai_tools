"""Plugin registry for agent extensions."""

_registry = {}

def register(name: str, fn):
    _registry[name] = fn


def list_plugins():
    return list(_registry.keys())

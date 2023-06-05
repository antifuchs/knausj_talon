from typing import Optional
from talon import ui, Module

mod = Module()

@mod.action_class
class Actions:
    def launch_and_activate(path: str):
        "Activate an application with the given path; launch if not running"
        return ui.launch(path=path)

    def just_activate(path: str):
        "Activate an app at the given path, if it's running"
        _just_activate(path=path)

    def just_activate_n(name: str):
        "Activate an app with the given name, if it's running"
        _just_activate(name=name)

    def just_activate_preferred(path1: str, path2: str):
        "Activate one of these apps, by order of preference, if they're running."
        for path in [path1, path2]:
            if _just_activate(path):
                return

def _just_activate(path: Optional[str] = None, name: Optional[str] = None) -> bool:
    "Activate an app at the given path, if it's running"
    if path is not None:
        app = running_app_by_path(path)
    elif name is not None:
        app = running_app_by_name(name)
    if app is not None:
        app.focus()
        return True
    return False

def running_app_by_path(path: str):
    "Returns the app matching the exact FS path given, or None if it's not running"
    return next((app for app in ui.apps() if app.path == path), None)

def running_app_by_name(name: str):
    "Returns the app matching the exact FS path given, or None if it's not running"
    return next((app for app in ui.apps() if app.name == name), None)

from typing import Optional
from talon import ui, Module
from ..core.windows_and_tabs import window_snap
from ..core.windows_and_tabs.window_snap import RelativeScreenPos

mod = Module()

# Copied from window_snap.py, but accessible here.
_snap_positions = {
    "left": RelativeScreenPos(0, 0, 0.5, 1),
    "right": RelativeScreenPos(0.5, 0, 1, 1),
    "full": RelativeScreenPos(0, 0, 1, 1),
}

@mod.action_class
class Actions:
    def translate_snap_name(name: str) -> RelativeScreenPos:
        "Translates a position name to a relative screen position."
        return _snap_positions[name]

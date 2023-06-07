from typing import Optional
from talon import ui, Module
from dataclasses import dataclass
from ..core.windows_and_tabs import window_snap
from ..core.windows_and_tabs.window_snap import RelativeScreenPos

mod = Module()

@dataclass
class VCRelativePos():
    zoom_main_pos: RelativeScreenPos
    zoom_aux_pos: RelativeScreenPos
    ft_pos: RelativeScreenPos

    zoom_main_monitor: int
    zoom_aux_monitor: int

    def move_windows(self):
        apps = [app for app in ui.apps() if app.name == "zoom.us"] + (
            [app for app in ui.apps() if app.name == "FaceTime"])
        if len(apps) == 0:
            return None
        app = apps[0]
        multi_screen = len(ui.screens()) > 1
        if app.name == "FaceTime":
            win = app.windows()[0]
            window_snap._snap_window_helper(win, pos=self.ft_pos)
        elif app.name == "zoom.us":
            main_wins = [win for win in app.windows() if win.title == "Zoom Meeting"]
            if len(main_wins) == 0:
                return
            main = main_wins[0]
            if multi_screen:
                window_snap._move_to_screen(main, screen_number=self.zoom_main_monitor)
            window_snap._snap_window_helper(main, self.zoom_main_pos)

            aux_wins = [win for win in app.windows() if win.title != "Zoom Meeting"]
            if len(aux_wins) == 0:
                return
            aux = aux_wins[0]
            if multi_screen:
                window_snap._move_to_screen(aux, screen_number=self.zoom_main_monitor)
            window_snap._snap_window_helper(aux, self.zoom_aux_pos)

_video_call_arrangements = {
    "one_on_one": VCRelativePos(
        zoom_main_pos=RelativeScreenPos(0.19,0.16,0.81,0.83),
        zoom_aux_pos=RelativeScreenPos(0.42,0,0.56,0.16),
        zoom_main_monitor=1,
        zoom_aux_monitor=1,
        ft_pos=RelativeScreenPos(0,0,1,1),
    ),
    "gallery": VCRelativePos(
        zoom_main_pos=RelativeScreenPos(0,0,0.55,1),
        zoom_aux_pos=RelativeScreenPos(0,0,1,1),
        zoom_main_monitor=1,
        zoom_aux_monitor=2,
        ft_pos=RelativeScreenPos(0,0,1,1),
    ),
    "screenshare": VCRelativePos(
        zoom_main_pos=RelativeScreenPos(0,0,1,1),
        zoom_aux_pos=RelativeScreenPos(0,0,1,1),
        zoom_main_monitor=2,
        zoom_aux_monitor=1,
        ft_pos=RelativeScreenPos(0,0,1,1),
    ),
}

@mod.action_class
class Actions:
    def translate_snap_name(name: str) -> RelativeScreenPos:
        "Translates a position name to a relative screen position."
        return window_snap._snap_positions[name]


    def layout_video_call_windows(arrangement_name: str):
        "Arranges video call windows in the requested layout"
        arrangement = _video_call_arrangements[arrangement_name]
        arrangement.move_windows()

def _find_video_chat_main_window():
    "Find the 'main' video chat window, facetime or zoom"
    apps = [app for app in ui.apps() if app.name == "zoom.us"] + (
        [app for app in ui.apps() if app.name == "FaceTime"])
    if len(apps) == 0:
        return None
    app = apps[0]
    # Find the main window:
    if app.name == "zoom.us":
        main = [win for win in app.windows() if win.title == "Zoom Meeting"]
        return main[0] if len(main) > 0 else None
    else:
        return app.windows()[0]

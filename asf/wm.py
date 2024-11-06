import time
from typing import Optional
from talon import ui, Module, actions, screen, cron, app
from talon.ui import App
from dataclasses import dataclass
from ..core.windows_and_tabs import window_snap
from ..core.windows_and_tabs.window_snap import RelativeScreenPos
from .app_layout.criteria import MimestreamMatch, WindowCriteria, EmacsMatch, NameMatch

mod = Module()

ZOOM_VIEW_OPTIONS_BUTTON_DESC="View"

@dataclass
class VCRelativePos():
    zoom_main_pos: RelativeScreenPos
    zoom_aux_pos: RelativeScreenPos
    ft_pos: RelativeScreenPos

    zoom_main_monitor: int
    zoom_aux_monitor: int

    zoom_switch_modes: Optional[str] = None

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
            if len(main_wins) >= 0:
                main = main_wins[0]
                if multi_screen:
                    window_snap._move_to_screen(main, screen_number=self.zoom_main_monitor)
                window_snap._snap_window_helper(main, self.zoom_main_pos)

            aux_wins = [win for win in app.windows() if win.title == "Zoom" and win.children[0].get("AXRoleDescription") == "video render"]
            print("aux windows", aux_wins)
            if len(aux_wins) > 0:
                aux = aux_wins[0]
                if multi_screen:
                    window_snap._move_to_screen(aux, screen_number=self.zoom_main_monitor)
                window_snap._snap_window_helper(aux, self.zoom_aux_pos)
            if self.zoom_switch_modes is not None:
                menu_bar = app.children.find_one(AXRole="AXMenuBar")
                meeting_menu = menu_bar.children.find_one(AXTitle="Meeting").children[0]
                try:
                    switcher = meeting_menu.children.find_one(AXTitle=self.zoom_switch_modes)
                    switcher.perform("AXPress")
                except ui.UIErr as e:
                    print(e, self.zoom_switch_modes, repr(meeting_menu), repr(meeting_menu.children))
                    # If the view is already active (or axkit can't find the menu entry
                    # yet), don't worry:
                    pass

_video_call_arrangements = {
    "one_on_one": VCRelativePos(
        zoom_main_pos=RelativeScreenPos(0.19,0.16,0.81,0.83),
        zoom_aux_pos=RelativeScreenPos(0.42,0,0.56,0.16),
        zoom_main_monitor=1,
        zoom_aux_monitor=1,
        zoom_switch_modes="Speaker View",
        ft_pos=RelativeScreenPos(0,0,1,1),
    ),
    "gallery": VCRelativePos(
        zoom_main_pos=RelativeScreenPos(0,0,0.55,1),
        zoom_aux_pos=RelativeScreenPos(0,0,1,1),
        zoom_main_monitor=1,
        zoom_aux_monitor=2,
        zoom_switch_modes="Gallery View",
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

@dataclass
class AppArrangement():
    app: str
    window: Optional[WindowCriteria]
    pos: RelativeScreenPos

_maximized=RelativeScreenPos(0, 0, 1, 1)

def _vertical_max(x0, xend):
    return RelativeScreenPos(x0, 0, xend, 1)

_app_arrangements = {
    'laptop': [
        AppArrangement(app="Mimestream", window=MimestreamMatch(False), pos=_maximized),
        AppArrangement(app="Mimestream", window=MimestreamMatch(True), pos=_vertical_max(0.2, 0.8)),
        AppArrangement(app="Emacs", window=EmacsMatch(), pos=_maximized),
        AppArrangement(app="Arc", window=None, pos=_maximized),
        AppArrangement(app="Slack", window=None, pos=_maximized),
        AppArrangement(app="iTerm2", window=None, pos=_maximized),
        AppArrangement(app="Messages", window=None, pos=_vertical_max(0, 0.35)),
        AppArrangement(app="Element", window=None, pos=_vertical_max(0, 0.8)),
        AppArrangement(app="Music", window=NameMatch("Music"), pos=_maximized)
    ],
    "large_screen": [
        AppArrangement(app="Mimestream", window=MimestreamMatch(), pos=_vertical_max(0.08, 0.59)),
        AppArrangement(app="Mimestream", window=MimestreamMatch(True), pos=_vertical_max(0.1, 0.4)),
        AppArrangement(app="Emacs", window=EmacsMatch(), pos=_maximized),
        AppArrangement(app="Arc", window=None, pos=_vertical_max(0.17, 0.85)),
        AppArrangement(app="Slack", window=None, pos=_vertical_max(0.55, 1)),
        AppArrangement(app="iTerm2", window=None, pos=_vertical_max(0, 0.5)),
        AppArrangement(app="Messages", window=None, pos=_vertical_max(0, 0.27)),
        AppArrangement(app="Element", window=None, pos=_vertical_max(0.05, 0.49)),
        AppArrangement(app="Music", window=NameMatch("Music"), pos=_vertical_max(0.19, 0.77))
    ],
    "multi_screen": [
        # TODO, same as single atm
        AppArrangement(app="Mimestream", window=MimestreamMatch(), pos=_vertical_max(0.08, 0.59)),
        AppArrangement(app="Mimestream", window=MimestreamMatch(True), pos=_vertical_max(0.1, 0.4)),
        AppArrangement(app="Emacs", window=EmacsMatch(), pos=_maximized),
        AppArrangement(app="Arc", window=None, pos=_vertical_max(0.17, 0.85)),
        AppArrangement(app="Slack", window=None, pos=_vertical_max(0.55, 1)),
        AppArrangement(app="iTerm2", window=None, pos=_vertical_max(0, 0.5)),
        AppArrangement(app="Messages", window=None, pos=_vertical_max(0, 0.27)),
        AppArrangement(app="Element", window=None, pos=_vertical_max(0.05, 0.49)),
        AppArrangement(app="Music", window=NameMatch("Music"), pos=_vertical_max(0.19, 0.77))
    ]
}

def _determine_layout():
    screens = screen.screens()
    main_screen = [scr for scr in screens if scr.main][0]
    if main_screen.mm_x < 500:
        return "laptop"
    elif len(screens) == 1:
        return "large_screen"
    else:
        return "multi_screen"

def _layout_app(window_style: AppArrangement,  app: App):
    app_hidden = app.element.AXHidden
    if app_hidden:
        app.element.AXHidden = False
        # wait until the windows' rects can be retrieved:
        for _ in range(20):
            try:
                for window in app.windows():
                    window.rect
            except AttributeError:
                time.sleep(0.1)
            else:
                break
    matching_windows = app.windows()
    if window_style.window is not None:
        matching_windows = window_style.window.matching_windows(matching_windows)
    for window in matching_windows:
        # acquire permission to move the window fast
        try:
            app_script = window.appscript()
            if hasattr(window, "bounds"):
                app_script.bounds()
        except AttributeError:
            pass
        window_snap._snap_window_helper(window, window_style.pos)
    app.element.AXHidden = app_hidden


@mod.action_class
class Actions:
    def translate_snap_name(name: str) -> RelativeScreenPos:
        "Translates a position name to a relative screen position."
        return window_snap._snap_positions[name]


    def layout_video_call_windows(arrangement_name: str):
        "Arranges video call windows in the requested layout"
        arrangement = _video_call_arrangements[arrangement_name]
        arrangement.move_windows()

    def layout_all_windows():
        "Arranges all windows according to their defined positions"
        arrangements = _app_arrangements[_determine_layout()]
        for window_style in arrangements:
            # find the app/window and then apply the size to it.
            for app in [app for app in ui.apps() if app.name == window_style.app]:
                _layout_app(window_style, app)

# Register our interest in newly-launched apps:
def _handle_app_launch(app):
    "Notices that an app was launched and puts its windows where we'd expect them."
    for window_style in _app_arrangements[_determine_layout()]:
        if window_style.app == app.name:
            # Give it 2 seconds to bring up a window:
            for _ in range(20):
                if len(app.windows()) > 0:
                    break
                time.sleep(0.1)
            _layout_app(window_style, app)

ui.register("app_launch", _handle_app_launch)


# Register our interest in screen arrangement changes:
def _handle_screen_change():
    layout = _determine_layout()
    if layout in _app_arrangements:
        for window_style in _app_arrangements[layout]:
            for app in [app for app in ui.apps() if app.name == window_style.app]:
                _layout_app(window_style, app)


def _listen_for_screen_change():
    _last_screen_config = []
    def _current_screens():
        return [(round(scr.mm_x), scr.main) for scr in screen.screens()]

    def _screen_change_check():
        nonlocal _last_screen_config
        if _current_screens() != _last_screen_config:
            print(f"Detected screen configuration change: {_last_screen_config} vs {_current_screens()}")
            _handle_screen_change()
        _last_screen_config = _current_screens()
    _screen_change_check()
    cron.interval("5s", _screen_change_check)

app.register("ready", _listen_for_screen_change)

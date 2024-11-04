from typing import Sequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from talon.ui import Window

class WindowCriteria(ABC):
    @abstractmethod
    def matching_windows(self, windows: Sequence[Window]) -> list[Window]:
        "Return all windows matching the given criteria."
        pass

@dataclass
class NameMatch(WindowCriteria):
    "Matches windows with the exact given name"

    title: str

    def matching_windows(self, windows: Sequence[Window]):
        return [win for win in windows if win.title == self.title]

class EmacsMatch(WindowCriteria):
    "Matches emacs windows that have a title bar (i.e., no posframes)"

    def matching_windows(self, windows: Sequence[Window]) -> list[Window]:
        return [win for win in windows if win.element.get('AXTitleUIElement', None) is not None]

@dataclass
class MimestreamMatch(WindowCriteria):
    "Matches the mimestream main window"

    compose_window: bool = field(default=False)

    def matching_windows(self, windows: Sequence[Window]) -> list[Window]:
        def _is_window_compose(win):
            return win.children[0].get('AXRoleDescription') == 'text'
        return [win for win in windows if _is_window_compose(win) == self.compose_window]

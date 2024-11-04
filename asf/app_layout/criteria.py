from typing import Sequence
from dataclasses import dataclass
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

from dataclasses import dataclass
from abc import ABC, abstractmethod
from talon.ui import Window

class WindowCriteria(ABC):
    @abstractmethod
    def matching_windows(self, windows: list[Window]) -> list[Window]:
        "Return all windows matching the given criteria."
        pass

@dataclass
class NameMatch(WindowCriteria):
    title: str

    def matching_windows(self, windows: list[Window]):
        return [win for win in windows if win.title == self.title]

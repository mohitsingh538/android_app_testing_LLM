from dataclasses import dataclass
from typing import Optional, List, Callable
from actions.open_app import OpenAppAction
from actions.search import SearchAction
from actions.take_screenshot import TakeScreenshotAction
from actions.wait_for_screen import WaitForScreenAction


@dataclass
class Action:
    name: str
    required_params: Optional[List[str]] = None
    description: str = ""
    function: Callable = None


action_handlers = {
    "open_app": Action(
        name="open_app",
        description="Opens a specified application",
        function=OpenAppAction
    ),

    "wait_for_screen": Action(
        name="wait_for_screen",
        description="Waits for a specific screen to load",
        function=WaitForScreenAction
    ),

    "take_screenshot": Action(
        name="take_screenshot",
        description="Takes a screenshot of the current screen",
        function=TakeScreenshotAction
    ),

    "search": Action(
        name="search",
        description="Performs a search using the search bar",
        required_params=["search_term"],
        function=SearchAction
    ),
}
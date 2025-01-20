


class BaseAction:

    def __init__(self, manager):
        self.manager = manager

    def execute(self, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")

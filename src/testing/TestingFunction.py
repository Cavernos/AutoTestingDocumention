class TestingFunction:
    def __init__(self, index: int, name: str, expected: list|str, enter_value: str):
        self.index = index
        self.name = name
        self.enter_value = enter_value
        self.expected = expected
        self._status: str = ""
        self.modification = []

    def to_csv(self):
        row = {}
        for i in range(len(self.__dict__.keys())):
            row[f"col{i+1}"] = getattr(self, f"{list(self.__dict__.keys())[i]}")
        return row
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

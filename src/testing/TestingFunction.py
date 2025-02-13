class TestingFunction:
    def __init__(self, index: int = 0, name: str = "", expected: list|str = "", enter_value: str = "", status: str = ""):
        self.index = index
        self.name = name
        self.enter_value = enter_value
        self.real_return_value = None
        self.expected = expected
        self.status: str = status
        self.modification = []

    def to_csv(self):
        row = {}
        for i in range(len(self.__dict__.keys())):
            row[f"col{i+1}"] = getattr(self, f"{list(self.__dict__.keys())[i]}")
        return row


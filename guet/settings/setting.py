class Setting:
    def __init__(self, default_value, parser, validator):
        self.default_value = default_value
        self.parser = parser
        self.validator = validator
        self.value = default_value

    def is_default_value(self) -> bool:
        return self.default_value == self.value

class FlyInError(Exception):
    pass


class MapParsingError(FlyInError):
    def __init__(self, reason: str, line_number: int | None = None) -> None:
        self.line_number = line_number
        self.reason = reason
        if line_number is not None:
            message = f"line {line_number}: {reason}"
        else:
            message = reason
        super().__init__(message)


class SimulationError(FlyInError):
    pass

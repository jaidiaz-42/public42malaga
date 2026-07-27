class Drone:
    def __init__(self, drone_id: str, path: list[str]) -> None:
        if len(path) < 1:
            raise ValueError("a drone needs a non-empty path")
        self.drone_id = drone_id
        self.path = path
        self.path_index = 0
        self.transit_remaining: int | None = None
        self.transit_connection_name: str | None = None
        self.last_move: str | None = None

    @property
    def current_zone(self) -> str:
        return self.path[self.path_index]

    @property
    def next_zone(self) -> str | None:
        if self.path_index + 1 >= len(self.path):
            return None
        return self.path[self.path_index + 1]

    @property
    def is_in_transit(self) -> bool:
        return self.transit_remaining is not None

    @property
    def is_delivered(self) -> bool:
        return self.path_index == len(self.path) - 1

    def start_transit(self, connection_name: str, turns: int) -> None:
        self.transit_connection_name = connection_name
        self.transit_remaining = turns

    def tick_transit(self) -> bool:
        assert self.transit_remaining is not None
        self.transit_remaining -= 1
        return self.transit_remaining == 0

    def complete_move(self) -> None:
        self.path_index += 1
        self.transit_remaining = None
        self.transit_connection_name = None

    def __repr__(self) -> str:
        return f"Drone({self.drone_id!r}, at={self.current_zone!r})"

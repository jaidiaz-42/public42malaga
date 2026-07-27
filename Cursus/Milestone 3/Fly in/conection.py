def make_key(zone_a: str, zone_b: str) -> tuple[str, str]:
    return (zone_a, zone_b) if zone_a < zone_b else (zone_b, zone_a)


class Connection:
    def __init__(
        self,
        zone_a: str,
        zone_b: str,
        max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.travelers: set[str] = set()

    @property
    def name(self) -> str:
        return f"{self.zone_a}-{self.zone_b}"

    @property
    def key(self) -> tuple[str, str]:
        return make_key(self.zone_a, self.zone_b)

    def other_end(self, zone_name: str) -> str:
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(f"{zone_name} is not an endpoint of {self.name}")

    def has_room_for(self, extra: int = 1) -> bool:
        return len(self.travelers) + extra <= self.max_link_capacity

    def enter(self, drone_id: str) -> None:
        self.travelers.add(drone_id)

    def leave(self, drone_id: str) -> None:
        self.travelers.discard(drone_id)

    def __repr__(self) -> str:
        return f"Connection({self.name!r}, cap={self.max_link_capacity})"

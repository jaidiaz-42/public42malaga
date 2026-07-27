from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

    @property
    def movement_cost(self) -> int:
        if self is ZoneType.RESTRICTED:
            return 2
        return 1

    @property
    def pathfinding_weight(self) -> float:
        if self is ZoneType.RESTRICTED:
            return 2.0
        if self is ZoneType.PRIORITY:
            return 0.999
        return 1.0


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.is_start = is_start
        self.is_end = is_end
        self.max_drones: float
        if is_start or is_end:
            self.max_drones = float("inf")
        else:
            self.max_drones = float(max_drones)
        self.occupants: set[str] = set()

    @property
    def is_blocked(self) -> bool:
        return self.zone_type is ZoneType.BLOCKED

    @property
    def available_capacity(self) -> float:
        return self.max_drones - len(self.occupants)

    def has_room_for(self, extra: int = 1) -> bool:
        return self.available_capacity >= extra

    def add_occupant(self, drone_id: str) -> None:
        self.occupants.add(drone_id)

    def remove_occupant(self, drone_id: str) -> None:
        self.occupants.discard(drone_id)

    def __repr__(self) -> str:
        return f"Zone({self.name!r}, type={self.zone_type.value})"

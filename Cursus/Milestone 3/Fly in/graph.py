from conection import Connection, make_key
from zone import Zone


class Graph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: dict[tuple[str, str], Connection] = {}
        self.adjacency: dict[str, list[str]] = {}
        self.start_name: str | None = None
        self.end_name: str | None = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        self.adjacency.setdefault(zone.name, [])
        if zone.is_start:
            self.start_name = zone.name
        if zone.is_end:
            self.end_name = zone.name

    def has_zone(self, name: str) -> bool:
        return name in self.zones

    def get_zone(self, name: str) -> Zone:
        return self.zones[name]

    def add_connection(self, connection: Connection) -> None:
        self.connections[connection.key] = connection
        self.adjacency[connection.zone_a].append(connection.zone_b)
        self.adjacency[connection.zone_b].append(connection.zone_a)

    def has_connection(self, zone_a: str, zone_b: str) -> bool:
        return make_key(zone_a, zone_b) in self.connections

    def get_connection(self, zone_a: str, zone_b: str) -> Connection:
        return self.connections[make_key(zone_a, zone_b)]

    def neighbors(self, zone_name: str) -> list[str]:
        return self.adjacency.get(zone_name, [])

    def get_start(self) -> Zone:
        assert self.start_name is not None
        return self.zones[self.start_name]

    def get_end(self) -> Zone:
        assert self.end_name is not None
        return self.zones[self.end_name]

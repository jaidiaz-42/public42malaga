import re

from exceptions import MapParsingError
from conection import Connection
from graph import Graph
from zone import Zone, ZoneType

ZONE_LINE_RE = re.compile(
    r"^(start_hub|end_hub|hub):\s*(\S+)\s+(-?\d+)\s+(-?\d+)"
    r"(?:\s*\[(.*)\])?\s*$"
)
CONNECTION_LINE_RE = re.compile(
    r"^connection:\s*([^\-\s\[]+)-([^\-\s\[]+)(?:\s*\[(.*)\])?\s*$"
)
NB_DRONES_RE = re.compile(r"^nb_drones:\s*(\d+)\s*$")


class MapParser:
    def parse_file(self, path: str) -> tuple[Graph, int]:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
        return self.parse_lines(lines)

    def parse_lines(self, lines: list[str]) -> tuple[Graph, int]:
        graph = Graph()
        nb_drones: int | None = None
        seen_start = False
        seen_end = False
        for index, raw_line in enumerate(lines, start=1):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("nb_drones:"):
                nb_drones = self._parse_nb_drones(line, index)
                continue
            if line.startswith(("start_hub:", "end_hub:", "hub:")):
                zone, is_start, is_end = self._parse_zone_line(line, index)
                if graph.has_zone(zone.name):
                    raise MapParsingError(
                        f"duplicate zone name '{zone.name}'", index
                    )
                if is_start:
                    if seen_start:
                        raise MapParsingError(
                            "more than one start_hub found", index
                        )
                    seen_start = True
                if is_end:
                    if seen_end:
                        raise MapParsingError(
                            "more than one end_hub found", index
                        )
                    seen_end = True
                graph.add_zone(zone)
                continue
            if line.startswith("connection:"):
                self._parse_connection_line(line, index, graph)
                continue
            raise MapParsingError(f"unrecognized line '{line}'", index)
        if nb_drones is None:
            raise MapParsingError("missing nb_drones declaration")
        if not seen_start:
            raise MapParsingError("missing start_hub zone")
        if not seen_end:
            raise MapParsingError("missing end_hub zone")
        return graph, nb_drones

    def _parse_nb_drones(self, line: str, index: int) -> int:
        match = NB_DRONES_RE.match(line)
        if not match:
            raise MapParsingError("invalid nb_drones format", index)
        value = int(match.group(1))
        if value <= 0:
            raise MapParsingError("nb_drones must be positive", index)
        return value

    def _parse_zone_line(
        self, line: str, index: int
    ) -> tuple[Zone, bool, bool]:
        match = ZONE_LINE_RE.match(line)
        if not match:
            raise MapParsingError("invalid zone line format", index)
        prefix, name, x_str, y_str, metadata_str = match.groups()
        is_start = prefix == "start_hub"
        is_end = prefix == "end_hub"
        metadata = self._parse_metadata(metadata_str, index)
        zone_type = self._extract_zone_type(metadata, index)
        color = metadata.pop("color", None)
        max_drones = self._extract_max_drones(
            metadata, index, ignore_validation=is_start or is_end
        )
        if metadata:
            unknown = ", ".join(sorted(metadata))
            raise MapParsingError(f"unknown zone tag(s): {unknown}", index)
        zone = Zone(
            name=name,
            x=int(x_str),
            y=int(y_str),
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=is_start,
            is_end=is_end,
        )
        return zone, is_start, is_end

    def _extract_zone_type(
        self, metadata: dict[str, str], index: int
    ) -> ZoneType:
        raw_type = metadata.pop("zone", ZoneType.NORMAL.value)
        try:
            return ZoneType(raw_type)
        except ValueError:
            raise MapParsingError(f"invalid zone type '{raw_type}'", index)

    def _extract_max_drones(
        self,
        metadata: dict[str, str],
        index: int,
        ignore_validation: bool = False,
    ) -> int:
        raw_value = metadata.pop("max_drones", "1")
        if ignore_validation:
            return 1
        if not raw_value.isdigit() or int(raw_value) <= 0:
            raise MapParsingError(
                f"max_drones must be a positive integer, got "
                f"'{raw_value}'",
                index,
            )
        return int(raw_value)

    def _parse_connection_line(
        self, line: str, index: int, graph: Graph
    ) -> None:
        match = CONNECTION_LINE_RE.match(line)
        if not match:
            raise MapParsingError("invalid connection line format", index)
        zone_a, zone_b, metadata_str = match.groups()
        if not graph.has_zone(zone_a):
            raise MapParsingError(f"unknown zone '{zone_a}'", index)
        if not graph.has_zone(zone_b):
            raise MapParsingError(f"unknown zone '{zone_b}'", index)
        if graph.has_connection(zone_a, zone_b):
            raise MapParsingError(
                f"duplicate connection '{zone_a}-{zone_b}'", index
            )
        metadata = self._parse_metadata(metadata_str, index)
        raw_capacity = metadata.pop("max_link_capacity", "1")
        if not raw_capacity.isdigit() or int(raw_capacity) <= 0:
            raise MapParsingError(
                f"max_link_capacity must be a positive integer, got "
                f"'{raw_capacity}'",
                index,
            )
        if metadata:
            unknown = ", ".join(sorted(metadata))
            raise MapParsingError(
                f"unknown connection tag(s): {unknown}", index
            )
        connection = Connection(zone_a, zone_b, int(raw_capacity))
        graph.add_connection(connection)

    def _parse_metadata(
        self, metadata_str: str | None, index: int
    ) -> dict[str, str]:
        metadata: dict[str, str] = {}
        if not metadata_str:
            return metadata
        for token in metadata_str.split():
            if "=" not in token:
                raise MapParsingError(f"invalid metadata tag '{token}'",
                                      index)
            key, value = token.split("=", 1)
            if key in metadata:
                raise MapParsingError(f"duplicate tag '{key}'", index)
            metadata[key] = value
        return metadata

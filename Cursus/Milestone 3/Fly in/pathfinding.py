import heapq

from conection import Connection
from exceptions import SimulationError
from graph import Graph
from zone import Zone

CONGESTION_PENALTY = 3.0


class PathFinder:
    def shortest_path(
        self,
        graph: Graph,
        start: str,
        end: str,
        zone_load: dict[str, int] | None = None,
        connection_load: dict[tuple[str, str], int] | None = None,
    ) -> list[str]:
        zone_load = zone_load if zone_load is not None else {}
        connection_load = (
            connection_load if connection_load is not None else {}
        )
        distances: dict[str, float] = {start: 0.0}
        previous: dict[str, str] = {}
        visited: set[str] = set()
        heap: list[tuple[float, str]] = [(0.0, start)]
        while heap:
            dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            if node == end:
                break
            for neighbor in graph.neighbors(node):
                neighbor_zone = graph.get_zone(neighbor)
                if neighbor_zone.is_blocked:
                    continue
                connection = graph.get_connection(node, neighbor)
                weight = self._edge_weight(
                    neighbor_zone, connection, zone_load, connection_load
                )
                candidate = dist + weight
                if candidate < distances.get(neighbor, float("inf")):
                    distances[neighbor] = candidate
                    previous[neighbor] = node
                    heapq.heappush(heap, (candidate, neighbor))
        if end not in distances:
            raise SimulationError(f"no valid path from {start} to {end}")
        path = [end]
        while path[-1] != start:
            path.append(previous[path[-1]])
        path.reverse()
        return path

    def _edge_weight(
        self,
        neighbor_zone: Zone,
        connection: Connection,
        zone_load: dict[str, int],
        connection_load: dict[tuple[str, str], int],
    ) -> float:
        weight = neighbor_zone.zone_type.pathfinding_weight
        weight += self._congestion_penalty(
            zone_load.get(neighbor_zone.name, 0), neighbor_zone.max_drones
        )
        weight += self._congestion_penalty(
            connection_load.get(connection.key, 0),
            connection.max_link_capacity,
        )
        return weight

    @staticmethod
    def _congestion_penalty(load: int, capacity: float) -> float:
        if capacity <= 0 or capacity == float("inf"):
            return 0.0
        return (load // capacity) * CONGESTION_PENALTY

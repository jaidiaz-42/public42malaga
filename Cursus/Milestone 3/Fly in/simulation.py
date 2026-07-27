from conection import Connection
from drone import Drone
from graph import Graph
from pathfinding import PathFinder
from zone import ZoneType
from exceptions import SimulationError

MAX_TURNS = 100000


class Simulation:
    def __init__(self, graph: Graph, nb_drones: int) -> None:
        self.graph = graph
        finder = PathFinder()
        start = graph.get_start().name
        end = graph.get_end().name
        zone_load: dict[str, int] = {}
        connection_load: dict[tuple[str, str], int] = {}
        self.drones: list[Drone] = []
        for i in range(nb_drones):
            path = finder.shortest_path(
                graph, start, end, zone_load, connection_load
            )
            self.drones.append(Drone(f"D{i + 1}", path))
            for zone_name in path:
                zone_load[zone_name] = zone_load.get(zone_name, 0) + 1
            for zone_a, zone_b in zip(path, path[1:]):
                key = graph.get_connection(zone_a, zone_b).key
                connection_load[key] = connection_load.get(key, 0) + 1
        for drone in self.drones:
            graph.get_start().add_occupant(drone.drone_id)
        self.turns: list[list[str]] = []

    def _active_drones(self) -> list[Drone]:
        return [d for d in self.drones if not d.is_delivered]

    def _finish_transit(self, drone: Drone, moves: list[str]) -> None:
        next_name = drone.next_zone
        if next_name is None:
            raise SimulationError(
                f"{drone.drone_id} finished transit with no next zone"
            )
        connection = self.graph.get_connection(
            drone.current_zone, next_name
        )
        connection.leave(drone.drone_id)
        drone.complete_move()
        moves.append(f"{drone.drone_id}-{drone.current_zone}")

    def _try_move(
        self,
        drone: Drone,
        moves: list[str],
        transient: list[tuple[Connection, str]],
    ) -> bool:
        next_name = drone.next_zone
        if next_name is None:
            return False
        next_zone = self.graph.get_zone(next_name)
        connection = self.graph.get_connection(drone.current_zone, next_name)
        if not connection.has_room_for(1):
            return False
        if not next_zone.has_room_for(1):
            return False
        current_zone = self.graph.get_zone(drone.current_zone)
        current_zone.remove_occupant(drone.drone_id)
        next_zone.add_occupant(drone.drone_id)
        connection.enter(drone.drone_id)
        if next_zone.zone_type is ZoneType.RESTRICTED:
            drone.start_transit(connection.name, turns=1)
            moves.append(f"{drone.drone_id}-{connection.name}")
        else:
            drone.complete_move()
            moves.append(f"{drone.drone_id}-{next_zone.name}")
            transient.append((connection, drone.drone_id))
        return True

    def step(self) -> list[str]:
        moves: list[str] = []
        transient: list[tuple[Connection, str]] = []
        moved_ids: set[str] = set()
        ordered = sorted(self._active_drones(), key=lambda d: d.drone_id)
        for drone in ordered:
            if drone.is_in_transit:
                arrived = drone.tick_transit()
                if arrived:
                    self._finish_transit(drone, moves)
                else:
                    conn_name = drone.transit_connection_name
                    moves.append(f"{drone.drone_id}-{conn_name}")
                moved_ids.add(drone.drone_id)
        self._resolve_new_moves(ordered, moved_ids, moves, transient)
        for connection, drone_id in transient:
            connection.leave(drone_id)
        return moves

    def _resolve_new_moves(
        self,
        ordered: list[Drone],
        moved_ids: set[str],
        moves: list[str],
        transient: list[tuple[Connection, str]],
    ) -> None:
        pending = [
            drone
            for drone in ordered
            if drone.drone_id not in moved_ids and not drone.is_delivered
        ]
        progressed = True
        while pending and progressed:
            progressed = False
            still_pending = []
            for drone in pending:
                if self._try_move(drone, moves, transient):
                    progressed = True
                else:
                    still_pending.append(drone)
            pending = still_pending

    def run(self) -> list[list[str]]:
        turns_elapsed = 0
        while any(not d.is_delivered for d in self.drones):
            turns_elapsed += 1
            if turns_elapsed > MAX_TURNS:
                raise SimulationError(
                    "simulation did not converge within the turn limit"
                )
            moves = self.step()
            if moves:
                self.turns.append(moves)
        return self.turns

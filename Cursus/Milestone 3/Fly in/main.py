import argparse
import sys

from exceptions import FlyInError
from parser import MapParser
from simulation import Simulation
from visualizer import Visualizer


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fly-in")
    parser.add_argument("map_file")
    parser.add_argument("--no-color", action="store_true")
    return parser


def run(map_file: str, use_color: bool) -> int:
    map_parser = MapParser()
    try:
        graph, nb_drones = map_parser.parse_file(map_file)
        simulation = Simulation(graph, nb_drones)
        turns = simulation.run()
    except FlyInError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    visualizer = Visualizer(graph, use_color=use_color)
    for index, moves in enumerate(turns, start=1):
        visualizer.print_turn(index, moves)
    visualizer.print_summary(len(turns), nb_drones)
    return 0


def main() -> int:
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()
    return run(args.map_file, use_color=not args.no_color)


if __name__ == "__main__":
    sys.exit(main())

from graph import Graph

ANSI_RESET = "\033[0m"

COLOR_MAP = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "orange": "\033[38;5;208m",
    "purple": "\033[38;5;93m",
    "brown": "\033[38;5;94m",
    "black": "\033[38;5;236m",
    "gray": "\033[38;5;245m",
    "grey": "\033[38;5;245m",
    "gold": "\033[38;5;220m",
    "violet": "\033[38;5;177m",
    "crimson": "\033[38;5;161m",
    "maroon": "\033[38;5;88m",
    "darkred": "\033[38;5;124m",
    "lime": "\033[38;5;154m",
    "rainbow": "\033[38;5;201m",
}


class Visualizer:
    def __init__(self, graph: Graph, use_color: bool = True) -> None:
        self.graph = graph
        self.use_color = use_color

    def colorize(self, text: str, color_name: str | None) -> str:
        if not self.use_color or color_name is None:
            return text
        code = COLOR_MAP.get(color_name.lower())
        if code is None:
            return text
        return f"{code}{text}{ANSI_RESET}"

    def _entry_color(self, target_name: str) -> str | None:
        if self.graph.has_zone(target_name):
            return self.graph.get_zone(target_name).color
        return None

    def format_turn(self, turn_number: int, moves: list[str]) -> str:
        colored_entries = []
        for entry in moves:
            target_name = entry.split("-", 1)[1]
            color = self._entry_color(target_name)
            colored_entries.append(self.colorize(entry, color))
        prefix = self.colorize(f"[turn {turn_number}]", "cyan")
        return f"{prefix} {' '.join(colored_entries)}"

    def print_turn(self, turn_number: int, moves: list[str]) -> None:
        print(self.format_turn(turn_number, moves))

    def print_summary(self, total_turns: int, nb_drones: int) -> None:
        message = f"delivered {nb_drones} drone(s) in {total_turns} turn(s)"
        print(self.colorize(message, "green"))

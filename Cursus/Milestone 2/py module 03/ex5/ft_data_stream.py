import random
from typing import Generator, List, Tuple


def gen_event() -> Generator[Tuple[str, str], None, None]:
    players: List[str] = ["alice", "bob", "charlie", "dylan"]
    actions: List[str] = ["run", "eat", "sleep", "grab", "move", "climb"]
    while True:
        yield (random.choice(players), random.choice(actions))


# definir funcion, el flake8 le quita legibilidad
def consume_event(
    event_list: List[Tuple[str, str]]
) -> Generator[Tuple[str, str], None, None]:
    while event_list:
        index: int = random.randrange(len(event_list))
        yield event_list.pop(index)


def main() -> None:
    print("=== Game Data Stream Processor ===")
    event_gen: Generator[Tuple[str, str], None, None] = gen_event()
    for i in range(1000):
        name, action = next(event_gen)
        if i < 15 or i > 991:
            print(f"Event {i}: Player {name} did action {action}")
        elif i == 15:
            print("[...]")

    event_list: List[Tuple[str, str]] = []
    for _ in range(10):
        event_list.append(next(event_gen))
    print(f"\nBuilt list of 10 events: {event_list}\n")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()

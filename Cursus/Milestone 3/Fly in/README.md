*This project has been created as part of the 42 curriculum by
jaidiaz-.*

## Description

**Fly-in** is a fully object-oriented, typesafe Python simulation
that routes a fleet of autonomous drones from a start hub to an end
hub across a network of zones, without relying on any graph library
(no `networkx`, no `graphlib`).

The project reads a custom map file format describing:

- Zones (`start_hub`, `end_hub`, `hub`), each with coordinates, an
  optional color, a movement type (`normal`, `restricted`,
  `priority`, `blocked`), and an optional capacity (`max_drones`).
- Connections between zones, each with an optional simultaneous
  traversal capacity (`max_link_capacity`).

Given that network, the simulation moves every drone from the start
hub to the end hub turn by turn, respecting zone and connection
capacity limits, movement costs, and multi-turn transits through
`restricted` zones, while trying to minimize the total number of
turns needed to deliver the whole fleet.

## Instructions

```bash
make install                     # install flake8 + mypy
make run ARGS="path/to/map.txt"  # run the simulation
make run ARGS="path/to/map.txt --no-color"
make debug ARGS="path/to/map.txt"  # run under pdb
make lint                        # flake8 + mypy (mandatory flags)
make lint-strict                 # flake8 + mypy --strict
make clean                       # remove __pycache__ / .mypy_cache
```

You can also run it directly:

```bash
python3 main.py path/to/map.txt [--no-color]
```

Example map files can be written following the format described in
the subject (Chapter VI, "Let the drone fly").

## Algorithm choices and implementation strategy

- **Parsing** (`parser.py`): a small line-oriented parser built on
  three regular expressions (`nb_drones:`, zone lines, connection
  lines). Each line is validated independently and any violation of
  the format raises a `MapParsingError` carrying the offending line
  number, so the program never crashes on a malformed map — it
  reports a clear error and exits with status 1. Per the subject,
  `max_drones` on the `start_hub`/`end_hub` is parsed but never
  validated nor enforced, since those zones always have unlimited
  capacity.

- **Graph** (`graph.py`, `conection.py`, `zone.py`): a plain
  adjacency-list graph implemented from scratch. `Connection.key`
  normalizes `(a, b)`/`(b, a)` into a single order-independent
  identifier so a link is only ever stored once.

- **Pathfinding** (`pathfinding.py`): Dijkstra's algorithm
  implemented with a binary heap (`heapq`), giving
  **O((V + E) log V)** per path computed. `restricted` zones weigh
  2, `priority` zones weigh a hair less than `normal` zones (0.999
  vs 1) so that, on ties, the pathfinder prefers routing drones
  through them, as suggested by the subject, without changing their
  real in-simulation cost (which stays exactly 1 turn — the
  `pathfinding_weight` used for ranking routes is deliberately kept
  separate from `movement_cost`, which drives the actual turn
  accounting in `simulation.py`).

  To satisfy the "distribution of drones across multiple paths"
  requirement, paths are **not** all computed once and shared: each
  drone gets its own path, computed one at a time. As drones are
  routed, the zones and connections they use accumulate a "load"
  counter; any zone/connection loaded past its capacity becomes
  progressively more expensive for the *next* drone's pathfinding
  call. This is a simple, general congestion-aware greedy scheduler:
  it needs no extra library, degrades gracefully to a single shared
  path when the map has no real alternative route, and automatically
  spreads drones over parallel branches (forks, loops, etc.) when
  one exists.

- **Simulation** (`simulation.py`): turns are resolved in two
  phases. First, drones already mid-flight through a `restricted`
  connection tick down their remaining transit time and either land
  or keep flying (they can never idle mid-connection, per the
  subject). Second, every other active drone attempts to move
  towards the next zone on its path. A drone's move can be blocked
  by zone or connection capacity; blocked drones are retried in a
  fixed-point loop within the *same* turn, so that a drone waiting
  to enter a zone that another drone is vacating that very turn
  still gets to move — exactly what "drones moving out of a zone
  free up capacity for that same turn" requires. A turn stops
  retrying once a full pass makes no further progress, which also
  guards against infinite loops when a genuine capacity deadlock
  occurs (on top of the global `MAX_TURNS` safety net, which raises
  a `SimulationError` instead of looping forever).

- **Complexity**: computing all `nb_drones` initial paths costs
  `O(nb_drones * (V + E) log V)`. Each simulation turn is
  `O(active drones)` in the common case; the fixed-point retry loop
  only re-examines drones that were actually blocked, so it does not
  change the overall complexity class for typical maps. Paths are
  computed once per drone up front and then simply walked turn by
  turn (no per-turn recomputation), which keeps memory usage at
  `O(V + E + nb_drones)`.

## Visual representation

`visualizer.py` prints one line per simulation turn to the terminal,
listing every drone move in the `D<id>-<destination>` format required
by the subject. Each destination is colored using the zone's
`color` metadata from the map file (ANSI 256-color codes), so
different zones are visually distinguishable at a glance; the
`[turn N]` prefix is highlighted separately, and a green summary
line reports the total turn count at the end. Color can be disabled
with `--no-color` for plain-text output or non-color terminals.

## Resources

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

**AI usage:** AI assistance (Claude) was used to review the existing
codebase for bugs, spec-compliance gaps, and mypy/flake8 issues, and
to help design and document the congestion-aware routing strategy
and the same-turn vacancy fix in the simulation loop. Every change
was reviewed and tested manually against the subject's rules before
being kept.
"""
generator.py — Reproducible random road-network generator.

We model a city as a *random geometric graph*: intersections are points scattered
in a square, and each intersection is wired to its k nearest neighbours by a road.
This mimics real road topology (nearby places are connected; the graph is sparse
and planar-ish) far better than an Erdos-Renyi random graph, and — crucially — it
gives every vertex real coordinates, so the A* straight-line heuristic is meaningful.

Edge weight model (so the A* heuristic stays ADMISSIBLE):
    w(u, v) = euclidean(u, v) * congestion,   congestion ~ Uniform[1.0, CONG_MAX]
Because every edge costs at least its straight-line length, the straight-line
distance to the target is a valid lower bound on the true remaining cost.

All randomness flows through a single seeded numpy Generator, so a given
(n, seed) always yields the identical graph -> fully reproducible benchmarks.

scipy.spatial.cKDTree is used ONLY as a supporting structure for fast nearest-
neighbour lookup during generation; it is NOT part of any graphed algorithm.
"""

from __future__ import annotations
from typing import Tuple
import numpy as np
from scipy.spatial import cKDTree

from .graph import Graph

CONG_MAX = 1.6          # maximum congestion multiplier on an edge
DEFAULT_K = 6           # nearest neighbours wired per intersection


def generate_road_network(n: int, seed: int, k: int = DEFAULT_K,
                          side: float = 1000.0) -> Graph:
    """
    Build a connected, undirected, weighted road network with `n` intersections.

    Returns a Graph with |E| ~ (k/2)*n undirected edges (after dedup), guaranteed
    connected so that every source->target query is well-defined.
    """
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0.0, side, size=(n, 2))

    g = Graph(n)
    for v in range(n):
        g.set_coord(v, float(coords[v, 0]), float(coords[v, 1]))

    # k-nearest-neighbour wiring (query k+1 because the nearest point is self).
    tree = cKDTree(coords)
    kq = min(k + 1, n)
    _, idx = tree.query(coords, k=kq)
    idx = np.atleast_2d(idx)

    seen: set[Tuple[int, int]] = set()
    for u in range(n):
        for j in range(1, kq):                 # skip column 0 (self)
            v = int(idx[u, j])
            if v == u:
                continue
            key = (u, v) if u < v else (v, u)
            if key in seen:
                continue
            seen.add(key)
            dist = float(np.hypot(coords[u, 0] - coords[v, 0],
                                  coords[u, 1] - coords[v, 1]))
            congestion = float(rng.uniform(1.0, CONG_MAX))
            g.add_edge(u, v, dist * congestion)

    _ensure_connected(g, coords, rng)
    return g


def _ensure_connected(g: Graph, coords: np.ndarray, rng: np.random.Generator) -> None:
    """Link any disconnected components so the whole network is reachable."""
    comp = _components(g)
    num_comp = max(comp) + 1
    if num_comp == 1:
        return
    # Connect each component's representative to component 0 with one real edge.
    rep = [-1] * num_comp
    for v, c in enumerate(comp):
        if rep[c] == -1:
            rep[c] = v
    base = rep[0]
    for c in range(1, num_comp):
        u, v = rep[c], base
        dist = float(np.hypot(coords[u, 0] - coords[v, 0],
                              coords[u, 1] - coords[v, 1]))
        congestion = float(rng.uniform(1.0, CONG_MAX))
        g.add_edge(u, v, dist * congestion)


def _components(g: Graph) -> list[int]:
    """Label connected components with an iterative DFS. Returns comp-id per vertex."""
    comp = [-1] * g.n
    cid = 0
    for s in range(g.n):
        if comp[s] != -1:
            continue
        stack = [s]
        comp[s] = cid
        while stack:
            u = stack.pop()
            for v, _w in g.adj[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp


def pick_source_target(g: Graph, seed: int) -> Tuple[int, int]:
    """
    Deterministically pick a far-apart (source, target) pair for a query.
    We pick the source, then the geometrically farthest vertex as target so the
    route is long and the algorithms do real work.
    """
    rng = np.random.default_rng(seed ^ 0x9E3779B9)
    src = int(rng.integers(0, g.n))
    best, best_d = src, -1.0
    for v in range(g.n):
        d = g.euclidean(src, v)
        if d > best_d:
            best_d, best = d, v
    return src, best

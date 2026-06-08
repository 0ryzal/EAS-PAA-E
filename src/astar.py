"""
astar.py — Algorithm C (bonus: a third, qualitatively different algorithm).

A* is an *informed* point-to-point search: it is Dijkstra guided by a heuristic
h(v) that estimates the remaining cost from v to the target. It pops vertices in
order of f(v) = g(v) + h(v), so it expands far fewer nodes than Dijkstra while
still returning the optimal path — provided h is ADMISSIBLE (never overestimates).

Our heuristic is the straight-line (Euclidean) distance to the target. Because
every edge costs at least its straight-line length (w = length x congestion,
congestion >= 1), the straight-line distance is a lower bound on the true cost,
hence admissible; it is also CONSISTENT, so each vertex is finalised once.

This is OUR OWN code; the only library used is our hand-written MinHeap.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import math

from .graph import Graph
from .minheap import MinHeap

INF = math.inf


@dataclass
class AStarResult:
    dist: List[float]          # g-value: best known cost from source
    parent: List[int]
    expanded: int              # vertices finalised (the key A* advantage vs Dijkstra)
    found: bool


def astar(g: Graph, source: int, target: int) -> AStarResult:
    n = g.n
    gscore = [INF] * n
    parent = [-1] * n
    settled = [False] * n
    gscore[source] = 0.0

    pq = MinHeap()
    pq.push(g.euclidean(source, target), source)   # f = g(=0) + h(source)
    expanded = 0
    found = False

    while not pq.is_empty():
        _f, u = pq.pop_min()
        if settled[u]:
            continue                               # stale entry -> skip
        settled[u] = True
        expanded += 1
        if u == target:
            found = True
            break

        gu = gscore[u]
        for v, w in g.adj[u]:
            if settled[v]:
                continue
            ng = gu + w
            if ng < gscore[v]:                     # relaxation on g-value
                gscore[v] = ng
                parent[v] = u
                f = ng + g.euclidean(v, target)    # admissible heuristic
                pq.push(f, v)

    return AStarResult(gscore, parent, expanded, found)

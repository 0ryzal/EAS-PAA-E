"""
dijkstra.py — Algorithm A (the core, non-trivial algorithm).

Dijkstra's single-source shortest-path algorithm with a binary min-heap and lazy
deletion. Correct for graphs with non-negative edge weights (our travel costs are
distances x congestion >= 0). For a point-to-point query we early-exit the moment
the target is finalised, which is a valid optimisation: once a vertex is popped its
tentative distance is final, so the target's distance never improves afterwards.

This is OUR OWN code; the only library used is our hand-written MinHeap.

Returns a Result with:
    dist[]   final shortest distance from source to every settled vertex (inf if unreached)
    parent[] predecessor on a shortest path (for route reconstruction)
    expanded number of vertices popped-and-settled (work measure)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import math

from .graph import Graph
from .minheap import MinHeap

INF = math.inf


@dataclass
class Result:
    dist: List[float]
    parent: List[int]
    expanded: int


def dijkstra(g: Graph, source: int, target: Optional[int] = None) -> Result:
    n = g.n
    dist = [INF] * n
    parent = [-1] * n
    settled = [False] * n      # True once a vertex is popped with its final distance
    dist[source] = 0.0

    pq = MinHeap()
    pq.push(0.0, source)
    expanded = 0

    while not pq.is_empty():
        d, u = pq.pop_min()
        if settled[u]:
            continue           # stale heap entry (lazy deletion) -> skip
        settled[u] = True
        expanded += 1
        if target is not None and u == target:
            break              # final distance to target found; stop early

        for v, w in g.adj[u]:
            if settled[v]:
                continue
            nd = d + w
            if nd < dist[v]:   # relaxation
                dist[v] = nd
                parent[v] = u
                pq.push(nd, v)

    return Result(dist, parent, expanded)


def reconstruct_path(parent: List[int], source: int, target: int) -> List[int]:
    """Walk parent[] pointers from target back to source. Empty list if unreachable."""
    if parent[target] == -1 and source != target:
        return []
    path = [target]
    while path[-1] != source:
        p = parent[path[-1]]
        if p == -1:
            return []          # unreachable
        path.append(p)
    path.reverse()
    return path

"""
bellman_ford.py — Algorithm B (the baseline / correctness oracle).

Bellman-Ford computes single-source shortest paths by relaxing EVERY edge,
repeatedly, up to |V|-1 times. It is slower than Dijkstra (O(V*E) vs
O((V+E) log V)) but needs no priority queue and, unlike Dijkstra, tolerates
negative edge weights and can detect negative cycles. On our non-negative road
networks it must return exactly the same distances as Dijkstra, which makes it a
perfect independent oracle for the correctness cross-check (Report §3, A5).

Two standard speed-ups that do NOT change the asymptotics or the result:
  * early termination: stop as soon as a full pass relaxes nothing (converged);
  * we iterate over a precomputed directed-arc list for cache-friendliness.

This is OUR OWN code.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import math

from .graph import Graph

INF = math.inf


@dataclass
class BFResult:
    dist: List[float]
    parent: List[int]
    passes: int                 # how many relaxation passes were actually run
    negative_cycle: bool


def _arc_list(g: Graph) -> List[Tuple[int, int, float]]:
    arcs: List[Tuple[int, int, float]] = []
    for u in range(g.n):
        for v, w in g.adj[u]:
            arcs.append((u, v, w))
    return arcs


def bellman_ford(g: Graph, source: int) -> BFResult:
    n = g.n
    dist = [INF] * n
    parent = [-1] * n
    dist[source] = 0.0
    arcs = _arc_list(g)

    passes = 0
    for _ in range(n - 1):
        passes += 1
        changed = False
        for u, v, w in arcs:
            du = dist[u]
            if du != INF and du + w < dist[v]:   # relaxation
                dist[v] = du + w
                parent[v] = u
                changed = True
        if not changed:
            break                                # converged early

    # One more pass: any further relaxation would indicate a negative cycle.
    negative_cycle = False
    for u, v, w in arcs:
        du = dist[u]
        if du != INF and du + w < dist[v]:
            negative_cycle = True
            break

    return BFResult(dist, parent, passes, negative_cycle)

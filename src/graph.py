"""
graph.py — Weighted, undirected road-network graph (adjacency-list form).

Model (see Report §1):
    V  = road intersections / nodes, each with a 2-D coordinate (metres).
    E  = bidirectional road segments between intersections.
    w  = travel "cost" of a segment (here: geometric length x congestion >= 0).
    source = the ambulance station; target = the incident location.

We store the graph as an adjacency list because real road networks are SPARSE
(|E| = O(|V|)); an adjacency matrix would waste O(V^2) memory and make Dijkstra's
neighbour scan O(V) per vertex instead of O(deg(v)).
"""

from __future__ import annotations
from typing import List, Tuple
import math


class Graph:
    """An undirected weighted graph with 2-D vertex coordinates."""

    __slots__ = ("n", "xs", "ys", "adj", "m")

    def __init__(self, n: int) -> None:
        self.n: int = n
        self.xs: List[float] = [0.0] * n          # x-coordinate of each vertex
        self.ys: List[float] = [0.0] * n          # y-coordinate of each vertex
        # adj[u] = list of (v, weight) outgoing arcs from u.
        self.adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        self.m: int = 0                           # number of undirected edges

    def set_coord(self, v: int, x: float, y: float) -> None:
        self.xs[v] = x
        self.ys[v] = y

    def add_edge(self, u: int, v: int, w: float) -> None:
        """Add an undirected edge u<->v with weight w (stored as two arcs)."""
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
        self.m += 1

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self.adj[u]

    def euclidean(self, u: int, v: int) -> float:
        """Straight-line distance between two vertices (used by the A* heuristic)."""
        dx = self.xs[u] - self.xs[v]
        dy = self.ys[u] - self.ys[v]
        return math.hypot(dx, dy)

    @property
    def num_arcs(self) -> int:
        """Total directed arcs stored (= 2 * number of undirected edges)."""
        return 2 * self.m

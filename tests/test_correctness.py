#!/usr/bin/env python3
"""
test_correctness.py — Correctness tests for the three algorithms.

Run:  python -m tests.test_correctness     (or: python tests/test_correctness.py)

Covers:
  1. A hand-built tiny graph with a KNOWN shortest distance.
  2. Cross-check on many random instances: Dijkstra == Bellman-Ford == A*
     on the queried (source, target) distance, and Dijkstra == Bellman-Ford
     on EVERY vertex's distance.
  3. The MinHeap returns items in non-decreasing priority order.
"""

from __future__ import annotations
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import Graph
from src.generator import generate_road_network, pick_source_target
from src.dijkstra import dijkstra, reconstruct_path
from src.bellman_ford import bellman_ford
from src.astar import astar
from src.minheap import MinHeap

EPS = 1e-6
_failures = 0


def check(cond: bool, msg: str) -> None:
    global _failures
    status = "ok  " if cond else "FAIL"
    if not cond:
        _failures += 1
    print(f"  [{status}] {msg}")


def test_known_small() -> None:
    """A 5-vertex graph whose source->target shortest cost we know by hand."""
    print("Test 1: known tiny graph")
    g = Graph(5)
    # Lay vertices on a line so Euclidean heuristic is valid; override weights.
    for v in range(5):
        g.set_coord(v, float(v), 0.0)
    g.add_edge(0, 1, 4.0)
    g.add_edge(0, 2, 1.0)
    g.add_edge(2, 1, 2.0)   # 0->2->1 costs 3, cheaper than direct 0->1 (4)
    g.add_edge(1, 3, 1.0)
    g.add_edge(2, 3, 5.0)
    g.add_edge(3, 4, 3.0)
    # Shortest 0->4: 0-2-1-3-4 = 1+2+1+3 = 7
    r = dijkstra(g, 0, target=4)
    check(abs(r.dist[4] - 7.0) < EPS, f"Dijkstra cost 0->4 == 7 (got {r.dist[4]})")
    path = reconstruct_path(r.parent, 0, 4)
    check(path == [0, 2, 1, 3, 4], f"path == [0,2,1,3,4] (got {path})")
    rb = bellman_ford(g, 0)
    check(abs(rb.dist[4] - 7.0) < EPS, f"Bellman-Ford cost 0->4 == 7 (got {rb.dist[4]})")
    ra = astar(g, 0, 4)
    check(abs(ra.dist[4] - 7.0) < EPS, f"A* cost 0->4 == 7 (got {ra.dist[4]})")


def test_cross_check_random() -> None:
    """On random road networks all three must agree on the queried distance."""
    print("Test 2: cross-check on random networks")
    all_match = True
    full_match = True
    a_optimal = True
    for seed in range(20):
        n = random.Random(seed).randint(50, 400)
        g = generate_road_network(n, seed=seed)
        src, dst = pick_source_target(g, seed=seed)
        rd = dijkstra(g, src)                 # full SSSP (no early exit)
        rb = bellman_ford(g, src)
        ra = astar(g, src, dst)
        if abs(rd.dist[dst] - rb.dist[dst]) > 1e-6 * max(1.0, rd.dist[dst]):
            all_match = False
        if abs(rd.dist[dst] - ra.dist[dst]) > 1e-6 * max(1.0, rd.dist[dst]):
            a_optimal = False
        # Every reachable vertex must match between Dijkstra and Bellman-Ford.
        for v in range(g.n):
            dv, bv = rd.dist[v], rb.dist[v]
            if math.isinf(dv) and math.isinf(bv):
                continue
            if abs(dv - bv) > 1e-6 * max(1.0, abs(dv)):
                full_match = False
                break
    check(all_match, "Dijkstra == Bellman-Ford on queried target (20 instances)")
    check(a_optimal, "A* == Dijkstra on queried target (A* is optimal)")
    check(full_match, "Dijkstra == Bellman-Ford on ALL vertices (20 instances)")


def test_minheap_order() -> None:
    print("Test 3: MinHeap pops in sorted order")
    rng = random.Random(123)
    vals = [rng.uniform(-100, 100) for _ in range(1000)]
    h = MinHeap()
    for i, x in enumerate(vals):
        h.push(x, i)
    out = []
    while not h.is_empty():
        p, _ = h.pop_min()
        out.append(p)
    check(out == sorted(vals), "popped order equals sorted(values)")


if __name__ == "__main__":
    test_known_small()
    test_cross_check_random()
    test_minheap_order()
    print()
    if _failures == 0:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print(f"{_failures} CHECK(S) FAILED")
        sys.exit(1)

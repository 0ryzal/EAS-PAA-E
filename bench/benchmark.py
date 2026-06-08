#!/usr/bin/env python3
"""
benchmark.py — Reproducible timing sweep for Report §3 (A4/A5).

For each input size n in a sweep spanning >= two orders of magnitude, we:
  * generate a road network with a FIXED seed (reproducible),
  * pick a far-apart (source, target) query,
  * time Dijkstra (point-to-point, early exit), Bellman-Ford (full SSSP), and
    A* (point-to-point), each averaged over REPEATS runs,
  * record the shortest-route cost from each algorithm and whether they AGREE
    (the correctness cross-check),
  * record work measures (nodes settled / relaxation passes).

Output: bench/results/timings.csv  (one row per size).

Run with one command via ../run_benchmark.sh, or directly:
    python -m bench.benchmark [--sizes 100,300,1000,3000,10000] [--repeats 5] [--seed 7]
"""

from __future__ import annotations
import argparse
import csv
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import generate_road_network, pick_source_target
from src.dijkstra import dijkstra
from src.bellman_ford import bellman_ford
from src.astar import astar

DEFAULT_SIZES = [100, 300, 1000, 3000, 10000]
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def time_call(fn, repeats: int) -> float:
    """Return the MEDIAN wall-clock time (seconds) over `repeats` runs."""
    samples = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - t0)
    return statistics.median(samples)


def run(sizes, repeats: int, seed: int) -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, "timings.csv")
    fields = ["n", "m", "arcs", "seed",
              "dijkstra_ms", "bellman_ms", "astar_ms",
              "dijkstra_settled", "astar_expanded", "bellman_passes",
              "cost_dijkstra", "cost_bellman", "cost_astar", "agree"]

    print(f"{'n':>7} {'m':>8} | {'Dijkstra':>10} {'Bellman':>10} {'A*':>10} "
          f"| {'A* exp':>8} {'Dij set':>8} | agree")
    print("-" * 80)

    rows = []
    for n in sizes:
        g = generate_road_network(n, seed=seed)
        src, dst = pick_source_target(g, seed=seed)

        # Correctness data (single run, exact values).
        rd = dijkstra(g, src, target=dst)
        rb = bellman_ford(g, src)
        ra = astar(g, src, dst)
        c_d, c_b, c_a = rd.dist[dst], rb.dist[dst], ra.dist[dst]
        tol = 1e-6 * max(1.0, c_d)
        agree = abs(c_d - c_b) < tol and abs(c_d - c_a) < tol

        # Timing (median of `repeats`).
        t_d = time_call(lambda: dijkstra(g, src, target=dst), repeats) * 1e3
        t_b = time_call(lambda: bellman_ford(g, src), repeats) * 1e3
        t_a = time_call(lambda: astar(g, src, dst), repeats) * 1e3

        row = {
            "n": n, "m": g.m, "arcs": g.num_arcs, "seed": seed,
            "dijkstra_ms": round(t_d, 4), "bellman_ms": round(t_b, 4),
            "astar_ms": round(t_a, 4),
            "dijkstra_settled": rd.expanded, "astar_expanded": ra.expanded,
            "bellman_passes": rb.passes,
            "cost_dijkstra": round(c_d, 6), "cost_bellman": round(c_b, 6),
            "cost_astar": round(c_a, 6), "agree": int(agree),
        }
        rows.append(row)
        print(f"{n:>7} {g.m:>8} | {t_d:>10.3f} {t_b:>10.3f} {t_a:>10.3f} "
              f"| {ra.expanded:>8} {rd.expanded:>8} | {'YES' if agree else 'NO'}")

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("-" * 80)
    print(f"Wrote {out_path}")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="SIGAP benchmark sweep")
    ap.add_argument("--sizes", type=str,
                    default=",".join(map(str, DEFAULT_SIZES)),
                    help="comma-separated input sizes")
    ap.add_argument("--repeats", type=int, default=5, help="runs per measurement")
    ap.add_argument("--seed", type=int, default=7, help="fixed random seed")
    args = ap.parse_args()
    sizes = [int(s) for s in args.sizes.split(",") if s.strip()]
    run(sizes, args.repeats, args.seed)


if __name__ == "__main__":
    main()

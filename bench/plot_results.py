#!/usr/bin/env python3
"""
plot_results.py — Turn bench/results/timings.csv into the figures used in §3.

Produces (in bench/results/):
  * runtime_vs_size.png   — log-log runtime vs n for all three algorithms,
                            with fitted empirical growth exponents (slopes).
  * work_vs_size.png      — nodes settled: A* vs Dijkstra (the informed-search win).

It also prints the fitted exponents so they can be quoted in the report (A5).
"""

from __future__ import annotations
import csv
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def fit_exponent(ns, ts):
    """Least-squares slope of log(t) vs log(n): the empirical growth exponent."""
    xs = [math.log(n) for n in ns]
    ys = [math.log(t) for t in ts]
    k = len(xs)
    mx = sum(xs) / k
    my = sum(ys) / k
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else float("nan")


def main():
    csv_path = os.path.join(RESULTS_DIR, "timings.csv")
    if not os.path.exists(csv_path):
        print(f"No data at {csv_path}. Run the benchmark first.", file=sys.stderr)
        sys.exit(1)
    rows = load(csv_path)
    ns = [int(r["n"]) for r in rows]
    dij = [float(r["dijkstra_ms"]) for r in rows]
    bel = [float(r["bellman_ms"]) for r in rows]
    ast = [float(r["astar_ms"]) for r in rows]

    e_dij = fit_exponent(ns, dij)
    e_bel = fit_exponent(ns, bel)
    e_ast = fit_exponent(ns, ast)
    print("Fitted empirical growth exponents (runtime ~ n^p):")
    print(f"  Dijkstra     p = {e_dij:.2f}   (theory ~1, near-linear on sparse graphs)")
    print(f"  Bellman-Ford p = {e_bel:.2f}   (theory ~2 on sparse graphs, V*E with E=O(V))")
    print(f"  A*           p = {e_ast:.2f}")

    # --- Figure 1: runtime vs size (log-log) ---
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.plot(ns, dij, "o-", color="#1f77b4", label=f"Dijkstra  (slope {e_dij:.2f})")
    ax.plot(ns, bel, "s-", color="#d62728", label=f"Bellman-Ford  (slope {e_bel:.2f})")
    ax.plot(ns, ast, "^-", color="#2ca02c", label=f"A*  (slope {e_ast:.2f})")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("number of intersections  n  (log scale)")
    ax.set_ylabel("query time  (ms, log scale)")
    ax.set_title("SIGAP — runtime vs network size")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    f1 = os.path.join(RESULTS_DIR, "runtime_vs_size.png")
    fig.savefig(f1, dpi=140)
    print(f"Wrote {f1}")

    # --- Figure 2: work (nodes settled) A* vs Dijkstra ---
    dij_set = [int(r["dijkstra_settled"]) for r in rows]
    ast_exp = [int(r["astar_expanded"]) for r in rows]
    fig2, ax2 = plt.subplots(figsize=(7.5, 5.5))
    ax2.plot(ns, dij_set, "o-", color="#1f77b4", label="Dijkstra nodes settled")
    ax2.plot(ns, ast_exp, "^-", color="#2ca02c", label="A* nodes expanded")
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel("number of intersections  n  (log scale)")
    ax2.set_ylabel("nodes expanded  (log scale)")
    ax2.set_title("SIGAP — search effort: A* vs Dijkstra")
    ax2.grid(True, which="both", ls=":", alpha=0.5)
    ax2.legend()
    fig2.tight_layout()
    f2 = os.path.join(RESULTS_DIR, "work_vs_size.png")
    fig2.savefig(f2, dpi=140)
    print(f"Wrote {f2}")


if __name__ == "__main__":
    main()

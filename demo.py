#!/usr/bin/env python3
"""
demo.py — End-to-end demonstration of the SIGAP emergency-dispatch router.

It generates a city road network, picks an ambulance station (source) and an
incident (target), then computes the fastest route with all three algorithms,
prints a side-by-side summary, cross-checks that they agree, and (optionally)
saves a PNG map with the route highlighted.

Usage:
    python demo.py [--n 1500] [--seed 42] [--no-plot] [--out demo_route.png]
"""

from __future__ import annotations
import argparse
import time

from src.generator import generate_road_network, pick_source_target
from src.dijkstra import dijkstra, reconstruct_path
from src.bellman_ford import bellman_ford
from src.astar import astar


def main() -> None:
    ap = argparse.ArgumentParser(description="SIGAP fastest-route dispatch demo")
    ap.add_argument("--n", type=int, default=1500, help="number of intersections")
    ap.add_argument("--seed", type=int, default=42, help="random seed")
    ap.add_argument("--no-plot", action="store_true", help="skip the map figure")
    ap.add_argument("--out", type=str, default="demo_route.png", help="figure path")
    args = ap.parse_args()

    print(f"Generating road network: n={args.n}, seed={args.seed} ...")
    g = generate_road_network(args.n, seed=args.seed)
    src, dst = pick_source_target(g, seed=args.seed)
    print(f"  |V|={g.n}  |E|={g.m}  arcs={g.num_arcs}")
    print(f"  Ambulance station (source) = {src}")
    print(f"  Incident (target)          = {dst}\n")

    # --- Algorithm A: Dijkstra (early-exit point-to-point) ---
    t0 = time.perf_counter()
    rd = dijkstra(g, src, target=dst)
    td = time.perf_counter() - t0

    # --- Algorithm B: Bellman-Ford (full SSSP oracle) ---
    t0 = time.perf_counter()
    rb = bellman_ford(g, src)
    tb = time.perf_counter() - t0

    # --- Algorithm C: A* (informed point-to-point) ---
    t0 = time.perf_counter()
    ra = astar(g, src, dst)
    ta = time.perf_counter() - t0

    path = reconstruct_path(rd.parent, src, dst)

    print("Fastest-route cost (lower is better):")
    print(f"  Dijkstra     : {rd.dist[dst]:.4f}   time={td*1e3:8.2f} ms"
          f"   settled={rd.expanded}")
    print(f"  Bellman-Ford : {rb.dist[dst]:.4f}   time={tb*1e3:8.2f} ms"
          f"   passes={rb.passes}")
    print(f"  A*           : {ra.dist[dst]:.4f}   time={ta*1e3:8.2f} ms"
          f"   expanded={ra.expanded}")

    # --- Correctness cross-check (Report §3, A5) ---
    eps = 1e-6
    agree = (abs(rd.dist[dst] - rb.dist[dst]) < eps and
             abs(rd.dist[dst] - ra.dist[dst]) < eps)
    print(f"\nCross-check (all three agree on cost): {'YES' if agree else 'NO'}")
    print(f"A* settled {ra.expanded} nodes vs Dijkstra {rd.expanded} "
          f"({100*ra.expanded/max(rd.expanded,1):.0f}% of Dijkstra's work)")
    print(f"Route length: {len(path)} intersections")

    if not args.no_plot:
        _plot(g, path, src, dst, args.out)
        print(f"\nSaved route map to {args.out}")


def _plot(g, path, src, dst, out_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 8))
    # Draw all road segments faintly.
    seen = set()
    for u in range(g.n):
        for v, _w in g.adj[u]:
            key = (u, v) if u < v else (v, u)
            if key in seen:
                continue
            seen.add(key)
            ax.plot([g.xs[u], g.xs[v]], [g.ys[u], g.ys[v]],
                    color="0.85", linewidth=0.4, zorder=1)
    # Highlight the chosen route.
    if path:
        px = [g.xs[v] for v in path]
        py = [g.ys[v] for v in path]
        ax.plot(px, py, color="crimson", linewidth=2.2, zorder=3,
                label=f"Fastest route ({len(path)} nodes)")
    ax.scatter([g.xs[src]], [g.ys[src]], c="green", s=120, marker="s",
               zorder=4, label="Station (source)")
    ax.scatter([g.xs[dst]], [g.ys[dst]], c="blue", s=120, marker="*",
               zorder=4, label="Incident (target)")
    ax.set_title(f"SIGAP fastest route — |V|={g.n}, |E|={g.m}")
    ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)


if __name__ == "__main__":
    main()

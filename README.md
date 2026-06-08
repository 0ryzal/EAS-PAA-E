# SIGAP — Fastest-Route Emergency Dispatch on City Road Networks

> EF234405 Design & Analysis of Algorithms — Final Exam (Group Capstone Project)
> **Design It · Prove It · Build It · Measure It**

SIGAP (*Sistem Informasi Gawat-darurat & Pencarian rute*) finds the **fastest
driving route** from an ambulance station to an incident on a city road network,
and compares three classic shortest-path algorithms — all implemented **from
scratch** — on the *same* instances:

| Role | Algorithm | Why |
|------|-----------|-----|
| **A — core** | **Dijkstra** (own binary min-heap) | non-negative weights, near-linear on sparse road graphs |
| **B — baseline / oracle** | **Bellman-Ford** | simple, no priority queue; independent correctness oracle |
| **C — bonus** | **A\*** (admissible straight-line heuristic) | informed search; same optimum, far fewer node expansions |

All three return the **identical** minimum-cost route on every instance (our
cross-check); Bellman-Ford is the slow-but-simple oracle, Dijkstra is the
work-horse, and A\* is the fastest by exploiting geometry.

---

## The problem, formally

Model the city as an undirected weighted graph `G = (V, E, w)`:

* **V** — road intersections, each with a 2-D coordinate (metres).
* **E** — bidirectional road segments.
* **w(e) ≥ 0** — travel cost of a segment = `geometric_length × congestion`,
  `congestion ∈ [1.0, 1.6]`. Because every edge costs *at least* its straight-line
  length, the straight-line distance to the target is an **admissible** A\* heuristic.
* **source** — the ambulance station; **target** — the incident.
* **Objective** — a minimum-total-cost path `source → target`.

See the full formal model, correctness proofs, and complexity analysis in
[`report/Report.pdf`](report/Report.pdf).

---

## Repository layout

```
src/
  minheap.py        binary min-heap priority queue (from scratch)
  graph.py          adjacency-list weighted graph + coordinates
  generator.py      reproducible random road-network generator (seeded)
  dijkstra.py       Algorithm A — Dijkstra (early-exit point-to-point)
  bellman_ford.py   Algorithm B — Bellman-Ford (SSSP oracle)
  astar.py          Algorithm C — A* (informed search)
demo.py             end-to-end CLI demo (+ route map PNG)
tests/
  test_correctness.py   known-answer + cross-check tests
bench/
  benchmark.py      timing sweep -> results/timings.csv
  plot_results.py   CSV -> runtime/work figures + fitted exponents
  results/          committed CSV and figures (deliverables)
report/
  build_report.py   regenerates Report.pdf with fpdf2
  Report.pdf        the submitted report
run_benchmark.sh    ONE command: tests + sweep + plots
```

## Requirements

* Python **3.10+** (developed and tested on **3.14.2**)
* `numpy`, `scipy`, `matplotlib` — install with:

```bash
pip install -r requirements.txt
```

`scipy.spatial.cKDTree` is used **only** for nearest-neighbour wiring while
*generating* the map; it is **not** part of any graph algorithm. The algorithmic
core (heap, Dijkstra, Bellman-Ford, A\*) is entirely our own code.

## Quick start

```bash
# 1. Run the interactive demo: build a city, route an ambulance, draw the map.
python demo.py --n 1500 --seed 42

# 2. Run the correctness tests (known answers + A/B/C cross-check).
python -m tests.test_correctness

# 3. Reproduce ALL benchmark data and figures with ONE command.
./run_benchmark.sh
```

`run_benchmark.sh` writes [`bench/results/timings.csv`](bench/results/timings.csv)
and the figures `runtime_vs_size.png` and `work_vs_size.png`. Sizes, repeats and
seed are configurable:

```bash
SIZES=100,300,1000,3000,10000 REPEATS=5 SEED=7 ./run_benchmark.sh
```

## Reproducibility

* **Fixed seeds.** Every map is generated from a single seeded `numpy` RNG, so a
  given `(n, seed)` always yields the identical graph. The benchmark seed is `7`.
* **One command.** `./run_benchmark.sh` regenerates the timing CSV and every plot.
* **Default sweep.** `n ∈ {100, 300, 1000, 3000, 10000}` — five sizes spanning two
  orders of magnitude, with `n = 10000 ≥ 1000` satisfying the scale requirement.

## Sample result (seed 7, 5-run median, this machine)

| n | m | Dijkstra (ms) | Bellman-Ford (ms) | A\* (ms) | A\* nodes / Dijkstra nodes | agree |
|------|-------|------|-------|------|------|-----|
| 100 | 365 | 0.12 | 0.17 | 0.09 | 55 / 100 | ✓ |
| 1000 | 3542 | 2.16 | 6.78 | 1.12 | 448 / 1000 | ✓ |
| 10000 | 35362 | 21.0 | 139.9 | 12.1 | 4654 / 9996 | ✓ |

Fitted empirical growth exponents: Dijkstra ≈ **1.11**, A\* ≈ **1.00**,
Bellman-Ford ≈ **1.42** — consistent with the analysis in §3 of the report.

## Rebuilding the report (optional)

```bash
pip install fpdf2
python report/build_report.py    # writes report/Report.pdf
```

## Attribution

* `numpy`, `scipy` (cKDTree for generation only), `matplotlib` (plotting),
  `fpdf2` (report build) — standard open-source libraries.
* Algorithms follow the standard formulations in Cormen, Leiserson, Rivest &
  Stein, *Introduction to Algorithms* (Dijkstra, Bellman-Ford) and Hart, Nilsson
  & Raphael (1968) for A\*. **All algorithmic code is our own.**

## License / academic integrity

Coursework for EF234405. The included worked specimen in the exam brief
(GridGuard/MST) is *not* used here; SIGAP solves a different problem
(point-to-point shortest path) with three original implementations.

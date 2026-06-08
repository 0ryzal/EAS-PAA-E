#!/usr/bin/env bash
# run_benchmark.sh — ONE command to reproduce all timing data and figures.
#
#   ./run_benchmark.sh
#
# It runs the correctness tests, the timing sweep (fixed seed), and the plots.
# Edit SIZES / REPEATS / SEED below to change the experiment.
set -euo pipefail
cd "$(dirname "$0")"

SIZES="${SIZES:-100,300,1000,3000,10000}"
REPEATS="${REPEATS:-5}"
SEED="${SEED:-7}"

echo "==> Correctness tests"
python3 -m tests.test_correctness

echo
echo "==> Benchmark sweep  (sizes=$SIZES, repeats=$REPEATS, seed=$SEED)"
python3 -m bench.benchmark --sizes "$SIZES" --repeats "$REPEATS" --seed "$SEED"

echo
echo "==> Plotting"
python3 -m bench.plot_results

echo
echo "Done. See bench/results/timings.csv and bench/results/*.png"

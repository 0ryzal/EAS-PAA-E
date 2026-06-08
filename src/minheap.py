"""
minheap.py — A binary min-heap priority queue, implemented from scratch.

This is a SUPPORTING data structure (the assignment explicitly permits using a
heap library), but we implement our own to keep the priority-queue logic fully
under our control and to make the (V + E) log V cost of Dijkstra/A* explicit.

The heap stores (priority, item) pairs and is array-backed. We use *lazy
deletion* in Dijkstra/A*: instead of decrease-key, we push a fresh (smaller-key,
vertex) entry and skip stale entries when they are popped. This keeps every
operation a clean O(log n) push/pop while still giving correct results.
"""

from __future__ import annotations
from typing import Any, List, Tuple


class MinHeap:
    """An array-backed binary min-heap keyed on `priority` (a float)."""

    __slots__ = ("_data",)

    def __init__(self) -> None:
        # Each element is a (priority, item) tuple. Index 0 is the root (min).
        self._data: List[Tuple[float, Any]] = []

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def push(self, priority: float, item: Any) -> None:
        """Insert `item` with the given `priority`. O(log n)."""
        data = self._data
        data.append((priority, item))
        self._sift_up(len(data) - 1)

    def pop_min(self) -> Tuple[float, Any]:
        """Remove and return the (priority, item) with the smallest priority. O(log n)."""
        data = self._data
        if not data:
            raise IndexError("pop_min from an empty heap")
        top = data[0]
        last = data.pop()           # remove final leaf
        if data:                    # move it to the root and sift down
            data[0] = last
            self._sift_down(0)
        return top

    # --- internal heap-maintenance helpers ---------------------------------

    def _sift_up(self, i: int) -> None:
        data = self._data
        item = data[i]
        while i > 0:
            parent = (i - 1) >> 1
            if data[parent][0] <= item[0]:
                break
            data[i] = data[parent]
            i = parent
        data[i] = item

    def _sift_down(self, i: int) -> None:
        data = self._data
        n = len(data)
        item = data[i]
        while True:
            left = 2 * i + 1
            right = left + 1
            smallest = i
            smallest_key = item[0]
            if left < n and data[left][0] < smallest_key:
                smallest = left
                smallest_key = data[left][0]
            if right < n and data[right][0] < smallest_key:
                smallest = right
            if smallest == i:
                break
            data[i] = data[smallest]
            i = smallest
        data[i] = item


---

#### nr_metric.py

```python
from dataclasses import dataclass
from typing import Callable, Tuple, List

# Authored by Nicholas Reid Angell — Nov 14, 2025 (EST)

MergeFn = Callable[[float, float], float]

def merge_sum(r: float, s: float) -> float:
    return r + s

def merge_max(r: float, s: float) -> float:
    return r if r >= s else s

@dataclass(frozen=True)
class NR:
    n: int
    r: float

    def add(self, other: "NR", merge: MergeFn) -> "NR":
        return NR(self.n + other.n, merge(self.r, other.r))

    def mul(self, other: "NR", merge: MergeFn) -> "NR":
        return NR(self.n * other.n, merge(self.r, other.r))

    def pow(self, k: int, merge: MergeFn) -> "NR":
        depth = self.r
        for _ in range(k - 1):
            depth = merge(depth, self.r)
        return NR(self.n ** k, depth)

def d_lambda(a: NR, b: NR, lam: float) -> float:
    return abs(a.n - b.n) + lam * abs(a.r - b.r)

def iso_depth(nodes: List[NR], target_r: float, tol: float = 1e-9) -> List[NR]:
    return [x for x in nodes if abs(x.r - target_r) <= tol]

def recursive_ratio(a: NR, delta: float, observable: Callable[[NR], float]) -> float:
    """R = F(n, r+delta) / F(n, r) for a chosen observable F."""
    top = observable(NR(a.n, a.r + delta))
    bottom = observable(a)
    if bottom == 0:
        return float("inf")
    return top / bottom

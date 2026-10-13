#!/usr/bin/env python3
"""Rank the most similar submission pairs for one problem (different users only).

    python3 analysis/similarity.py IC26BM            # top 30
    python3 analysis/similarity.py IC26AM 60         # top 60

Score = max(7-gram containment, token-sequence ratio) on names-ignored tokens, 0..1.
Empty templates / tiny stubs (< 120 tokens) are skipped.  A high score is a reason to LOOK at
two submissions, not proof of copying: short standard solutions score high on their own.
"""
import difflib, itertools, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load, substantial, status

prob = sys.argv[1]
top = int(sys.argv[2]) if len(sys.argv) > 2 else 30
N = substantial(load(prob))
print(f"{prob}: {len(N)} substantial submissions, {len({s['user'] for s in N})} users")
pairs = []
for a, b in itertools.combinations(N, 2):
    if a["user"] == b["user"] and a["user"] != "?":
        continue
    if abs(len(a["t"]) - len(b["t"])) > 0.5 * max(len(a["t"]), len(b["t"])):
        continue
    c = len(a["g"] & b["g"]) / max(1, min(len(a["g"]), len(b["g"])))
    if c < 0.35:
        continue
    q = difflib.SequenceMatcher(None, a["t"], b["t"], autojunk=False).ratio()
    pairs.append((max(c, q), c, q, a, b))
pairs.sort(key=lambda x: -x[0])
v = lambda s: "AC" if s["ac"] else ("WA" if s["ac"] is not None else "??")
for sc, c, q, a, b in pairs[:top]:
    print(f"{sc:.2f} (7g {c:.2f} seq {q:.2f})  {a['id']}[{v(a)}] {status(a)}  ~  {b['id']}[{v(b)}] {status(b)}")

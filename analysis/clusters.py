#!/usr/bin/env python3
"""Group near-identical submissions into clusters, tagged pool / excluded / unattributed.

    python3 analysis/clusters.py IC26BM 0.88

Two submissions by different users are linked when their similarity >= threshold; clusters are the
connected groups.  'reportable' = the cluster contains at least one team still in the Selection Pool.
For problems with a short standard solution (e.g. P8) big clusters just mean 'everyone wrote the
obvious formula'; read the code before drawing conclusions.
"""
import collections, difflib, itertools, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load, substantial, status

prob, thr = sys.argv[1], float(sys.argv[2])
S = {s["id"]: s for s in substantial(load(prob))}
par = {}
def find(x):
    while par.setdefault(x, x) != x:
        par[x] = par[par[x]]
        x = par[x]
    return x
for a, b in itertools.combinations(S.values(), 2):
    if a["user"] == b["user"] and a["user"] != "?":
        continue
    if abs(len(a["t"]) - len(b["t"])) > 0.5 * max(len(a["t"]), len(b["t"])):
        continue
    c = len(a["g"] & b["g"]) / max(1, min(len(a["g"]), len(b["g"])))
    if c < thr - 0.15:
        continue
    if max(c, difflib.SequenceMatcher(None, a["t"], b["t"], autojunk=False).ratio()) >= thr:
        par[find(a["id"])] = find(b["id"])
comp = collections.defaultdict(list)
for x in list(par):
    comp[find(x)].append(x)
clusters = [c for c in comp.values() if len({S[i]["user"] for i in c}) >= 2]
clusters.sort(key=lambda c: (-len({S[i]["user"] for i in c}), -len(c)))
print(f"{prob}, threshold {thr}: {len(clusters)} clusters (>= 2 users)")
for c in clusters:
    kinds = collections.Counter("POOL" if S[i]["rank"] else ("UNATTR" if S[i]["user"] == "?" else "EXCL") for i in c)
    print(f"\n== {len(c)} submissions, {len({S[i]['user'] for i in c})} users {dict(kinds)} reportable={'YES' if kinds['POOL'] else 'no'}")
    for i in sorted(c):
        s = S[i]
        print(f"   {i} {'AC' if s['ac'] else 'WA' if s['ac'] is not None else '??'} {s['lang']:6} {status(s)}")

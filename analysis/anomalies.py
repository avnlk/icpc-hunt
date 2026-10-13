#!/usr/bin/env python3
"""List teams that solved one of the hard problems (default P7-P10) while skipping >= 2 problems
that MORE teams solved ("easier" = solved by more teams).

    python3 analysis/anomalies.py                # writes anomaly_review_list_v2.csv
    python3 analysis/anomalies.py 7 2            # hardest-problem number >= 7, >= 2 skipped
    python3 analysis/anomalies.py 7 2 out.csv    # write somewhere else

Needs only selection_pool_2026-10-12.csv.  This is a reason to read a team's code, never evidence by itself.
(Problem 8 turned out to have a ~15-line solution, so skipping P6/P7 and solving P8 is plausible.)
"""
import collections, csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, POOL_CSV, PROBLEMS

min_hard = int(sys.argv[1]) if len(sys.argv) > 1 else 7
min_skip = int(sys.argv[2]) if len(sys.argv) > 2 else 2
dest = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "anomaly_review_list_v2.csv"
codes = [PROBLEMS[f"P{i}"] for i in range(1, 11)]
rows = list(csv.DictReader(open(POOL_CSV, encoding="utf-8-sig")))
ok = lambda r, p: r[p].strip() not in ("", "0", "0.0")
solvers = {p: sum(ok(r, p) for r in rows) for p in codes}
out = []
for r in rows:
    solved = [i + 1 for i, p in enumerate(codes) if ok(r, p)]
    hard = [i for i in solved if i >= min_hard]
    if not hard:
        continue
    h = min(hard, key=lambda i: solvers[codes[i - 1]])
    skipped = [f"P{i+1}({solvers[p]})" for i, p in enumerate(codes) if not ok(r, p) and solvers[p] > solvers[codes[h - 1]]]
    if len(skipped) >= min_skip:
        out.append(dict(rank=r["Rank"], username=r["Preliminary Username"], team=r["Team Name(s)"],
                        inst=r["Institute Name(s)"], solved=r["Problems Solved"],
                        solved_set=" ".join(map(str, solved)), hardest=f"P{h} ({solvers[codes[h-1]]} solvers)",
                        skipped=" ".join(skipped),
                        check_links=" ".join(f"https://www.codechef.com/ICPCOL2026/status/{codes[i-1]}?usernames={r['Preliminary Username']}"
                                             for i in solved if i >= 5)))
with open(dest, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print(len(out), "teams ->", dest)

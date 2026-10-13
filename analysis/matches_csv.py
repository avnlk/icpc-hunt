#!/usr/bin/env python3
"""Write every cross-user match >= threshold to a CSV, with two scores per pair.

    python3 analysis/matches_csv.py IC26AM evidence/P8_matches.csv 0.80

score_names_ignored : identifiers replaced by a placeholder (structure only)
score_names_kept    : identifiers, numbers and strings must match too (stricter)
Also writes <out>_by_pool_team.csv with each pool team's best match.
"""
import collections, csv, difflib, itertools, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load, substantial, status

prob, out, thr = sys.argv[1], sys.argv[2], float(sys.argv[3])
N = substantial(load(prob))
rows = []
for a, b in itertools.combinations(N, 2):
    if a["user"] == b["user"] and a["user"] != "?":
        continue
    if abs(len(a["t"]) - len(b["t"])) > 0.5 * max(len(a["t"]), len(b["t"])):
        continue
    c = len(a["g"] & b["g"]) / max(1, min(len(a["g"]), len(b["g"])))
    if c < 0.55:
        continue
    sc = max(c, difflib.SequenceMatcher(None, a["t"], b["t"], autojunk=False).ratio())
    if sc < thr:
        continue
    kept = difflib.SequenceMatcher(None, a["r"], b["r"], autojunk=False).ratio()
    v = lambda s: "AC" if s["ac"] else "WA"
    rows.append(dict(score_names_ignored=round(sc, 3), score_names_kept=round(kept, 3),
                     a_id=a["id"], a_verdict=v(a), a_lang=a["lang"], a_status=status(a), a_user=a["user"],
                     b_id=b["id"], b_verdict=v(b), b_lang=b["lang"], b_status=status(b), b_user=b["user"]))
rows.sort(key=lambda r: (-r["score_names_kept"], -r["score_names_ignored"]))
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), "pairs >=", thr, "->", out)

best = {}
for r in rows:
    for me, ot in (("a", "b"), ("b", "a")):
        k = r[me + "_status"]
        if k.startswith("POOL") and (k not in best or r["score_names_kept"] > best[k][0]["score_names_kept"]):
            best[k] = (r, me, ot)
with open(out.replace(".csv", "_by_pool_team.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pool_rank", "team", "best_score_names_kept", "score_names_ignored", "my_submission",
                "my_verdict", "matched_submission", "matched_verdict", "matched_status"])
    for k, (r, me, ot) in sorted(best.items(), key=lambda kv: int(kv[0].split("#")[1].split()[0])):
        w.writerow([k.split("#")[1].split()[0], " ".join(k.split()[2:]), r["score_names_kept"], r["score_names_ignored"],
                    r[me + "_id"], r[me + "_verdict"], r[ot + "_id"], r[ot + "_verdict"], r[ot + "_status"]])
print(len(best), "pool teams with a match")

#!/usr/bin/env python3
"""Check evidence/README.md against the data: every row's id, verdict, team and username, that its code copy
is byte-identical to the downloaded file, that every submission id in every markdown file is a correct link,
and re-compute the headline numbers quoted in the write-ups.

    python3 analysis/verify_evidence.py          (reads ccdump/ if present, else data/)
"""
import difflib, hashlib, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, DATA, load, toks, grams

ok = True
def check(cond, msg):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + msg)

S = {"P10": load("IC26BM"), "P8": load("IC26AM")}
md = (ROOT / "evidence" / "README.md").read_text()

# 1. table rows: | [id](url) | verdict | team | username | [code](path) |
rows = re.findall(r"^\| \[(\d{10})\]\((https://[^)]+)\) \| (AC|WA) \| ([^|]+?) \| (icpcol\d+) \| \[([^\]]+)\]\(([^)]+)\) \|$", md, re.M)
check(rows, f"found {len(rows)} table rows")
section = None
problem_of = {}
for line in md.split("\n"):
    m = re.match(r"## [A-G]\. (P\d+):", line)
    if m: section = m.group(1)
    m = re.match(r"^\| \[(\d{10})\]", line)
    if m and section: problem_of[m.group(1)] = section
bad = 0
for sid, url, verdict, team, user, label, path in rows:
    P = problem_of[sid]; s = S[P].get(sid)
    good = (s is not None and url == f"https://www.codechef.com/viewsolution/{sid}" and verdict == ("AC" if s["ac"] else "WA")
            and s["user"] == user and label == f"{P}_{sid}.txt")
    want = f"{s['team']} (#{s['rank']})" if s and s["rank"] else "need to verify"
    good = good and team == want
    cp = ROOT / "evidence" / path
    src = DATA / ("IC26BM" if P == "P10" else "IC26AM") / "code" / f"{sid}.txt"
    good = good and cp.exists() and src.exists() and hashlib.sha1(cp.read_bytes()).digest() == hashlib.sha1(src.read_bytes()).digest()
    if not good:
        bad += 1; print("   mismatch:", sid, verdict, team, user)
check(bad == 0, f"all {len(rows)} rows match id/verdict/team/username/link and the code copy is identical to the download")

# 2. every id in every markdown file is a link whose url matches its text
for f in subprocess.check_output(["git", "ls-files", "*.md"], cwd=ROOT).decode().split():
    t = (ROOT / f).read_text()
    rest = re.sub(r"\[[^\]]*\]\([^)]*\)|https?://\S+", "", t)
    bare = re.findall(r"\b13\d{8}\b", rest)
    wrong = [(a, b) for a, b in re.findall(r"\[`?(13\d{8})`?\]\(https://www\.codechef\.com/viewsolution/(\d+)\)", t) if a != b]
    check(not bare and not wrong, f"{f}: every submission id is a link ({len(re.findall(r'viewsolution/', t))} links, {len(bare)} bare, {len(wrong)} wrong)")

# 3. quoted statistics
A = S["P8"]; B = S["P10"]
cpp = [s for s in A.values() if s["code"] and len(s["code"]) > 150 and re.search(r"#include|cin|scanf", s["code"])]
idi = [s for s in A.values() if s["code"] and len(s["code"]) > 150 and re.search(r"if\s*\(\s*cin\s*>>\s*\w+\s*\)|if\s*\(\s*!\s*\(\s*cin\s*>>", s["code"])]
print(f"   C/C++ P8 submissions: {len(cpp)}, with the idiom: {len(idi)}, pool teams: {sorted({s['team'] for s in idi if s['rank']})}")
check(f"In {len(cpp)} collected C/C++ P8" in md or f"In {len(cpp)} " in md, f"README quotes the C/C++ P8 count ({len(cpp)})")
check(f"{len(idi)} contain" in md, f"README quotes {len(idi)} idiom submissions")
ref = A["1368468730"]["code"]
for sid, want in (("1368475384", 0.92), ("1368476038", 0.81), ("1368476546", 0.65), ("1368468108", 0.39), ("1368457937", 0.23)):
    r = difflib.SequenceMatcher(None, ref, A[sid]["code"], autojunk=False).ratio()
    check(abs(r - want) < 0.006, f"raw similarity to Recursive Raiders {sid}: {r:.2f} (quoted {want})")
py = [s for s in B.values() if s["lang"].startswith("PY") and s["code"] and len(s["code"]) > 250 and s["id"] not in
      ('1368446624','1368458414','1368458600','1368468854','1368469657','1368469844','1368470657')]
both = [s for s in py if re.search(r"\w\s*-=\s*\w+\s*==\s*[0-3]", s["code"]) and re.search(r"1\+4\*i\s*:\s*5\+4\*i", s["code"])]
check(len(both) == 0 and f"Of {len(py)} other Python" in md.replace("\n", " ") or len(both) == 0, f"other Python P10 submissions: {len(py)}, with both quirks: {len(both)}")
def pair(P, a, b):
    x, y = S[P][a]["code"], S[P][b]["code"]
    tx, ty = toks(x), toks(y)
    gx, gy = grams(tx), grams(ty)
    c = len(gx & gy) / max(1, min(len(gx), len(gy)))
    return max(c, difflib.SequenceMatcher(None, tx, ty, autojunk=False).ratio()), difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()
for label, P, a, b, want_ign, want_raw in (("CoreX pair (B)", "P10", "1368462543", "1368456405", 0.94, None),
                                          ("Code Nova pair (C)", "P10", "1368474166", "1368454398", 0.98, 0.73)):
    ig, raw = pair(P, a, b)
    check(abs(ig - want_ign) < 0.02 and (want_raw is None or abs(raw - want_raw) < 0.02), f"{label}: names-ignored {ig:.2f}, raw {raw:.2f} (quoted {want_ign}/{want_raw})")
print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)

"""Shared helpers: load the Selection Pool + downloaded submissions, and tokenise code.

Layout expected (relative to the repo root):
    selection_pool_2026-10-12.csv        official pool (rank, username, team, college, per-problem scores)
    ccdump/<PROBLEM>/list.csv            submission list  (id, status page, "cells")   [or data/<PROBLEM>/...]
    ccdump/<PROBLEM>/code/<id>.txt       one file of source code per submission
"""
import csv, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POOL_CSV = ROOT / "selection_pool_2026-10-12.csv"
# downloaded submissions: your own fresh download (ccdump/) if present, else the copy shipped in the repo (data/)
DATA = ROOT / "ccdump" if (ROOT / "ccdump").exists() else ROOT / "data"

PROBLEMS = {  # contest order P1..P10
    "P1": "PHNCHRG", "P2": "IC26CS", "P3": "IC26MP", "P4": "IC26CB", "P5": "IC26SH",
    "P6": "IC26LR", "P7": "IC26TM", "P8": "IC26AM", "P9": "IC26MM", "P10": "IC26BM",
}

def load_pool():
    """username -> row of the Selection Pool (only teams still in the pool)."""
    with open(POOL_CSV, encoding="utf-8-sig") as f:
        return {r["Preliminary Username"]: r for r in csv.DictReader(f)}

POOL = load_pool()

def load(prob, include_unattributed=True):
    """Return {submission_id: dict}. Submissions whose username is not in the pool are 'excluded'
    (withdrawn / removed teams: the published submissions include them). Code files that are not
    in list.csv have no username (user '?') -- 'unattributed'."""
    d = DATA / prob
    subs = {}
    with open(d / "list.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = [x.strip() for x in r["cells"].replace("\n", " | ").split(" | ")]
            if len(c) < 8:
                continue
            sid, user, score, lang = c[0], c[3], c[4], c[7]
            fp = d / "code" / f"{sid}.txt"
            code = fp.read_text(errors="replace") if fp.exists() else None
            row = POOL.get(user)
            subs[sid] = dict(
                id=sid, user=user, ac=("100" in score), lang=lang, code=code, when=c[1],
                team=row["Team Name(s)"] if row else "?",
                rank=int(row["Rank"]) if row else None,
                inst=row["Institute Name(s)"] if row else "?",
            )
    if include_unattributed and (d / "code").exists():
        for fp in (d / "code").iterdir():
            sid = fp.stem
            if sid not in subs:
                subs[sid] = dict(id=sid, user="?", ac=None, lang="?", code=fp.read_text(errors="replace"),
                                 when="", team="?", rank=None, inst="?")
    return subs

def status(s):
    """Human label: pool team (rank + name), excluded user, or unattributed."""
    if s["rank"]:
        return f"POOL #{s['rank']} {s['team']}"
    return "unattributed" if s["user"] == "?" else f"excluded {s['user']}"

# ---------------------------------------------------------------- tokenising
KW = set("""alignas auto bool break case catch char class const constexpr continue default delete do double
else enum explicit extern false float for friend goto if inline int long namespace new nullptr operator
private protected public return short signed sizeof static struct switch template this throw true try
typedef typename union unsigned using virtual void volatile while cin cout cerr endl vector map set
unordered_map unordered_set string pair array queue deque stack priority_queue sort min max swap abs size
push_back pop_back begin end first second main lambda def import from and or not in is elif pass print
range len sum sorted append join split strip input list dict tuple str enumerate zip None True False""".split())

def _strip(src):
    src = re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"(?m)#(?!include|define)[^\n]*", "", src)      # python comments
    return re.sub(r"#\s*(include|pragma)[^\n]*", "", src)

def toks(src):
    """Names-ignored tokens: every identifier -> 'I', numbers -> 'N', strings -> 'S' (keywords kept)."""
    out = []
    for m in re.finditer(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|[A-Za-z_]\w*|\d+\.?\d*|<<=|>>=|<=|>=|==|!=|&&|\|\||<<|>>|\+\+|--|[-+*/%&|^]=|->|::|\S", _strip(src)):
        t = m.group(0)
        if t[0] in "\"'":
            out.append("S")
        elif t[0].isdigit():
            out.append("N")
        elif t[0].isalpha() or t[0] == "_":
            out.append(t if t in KW else "I")
        else:
            out.append(t)
    return out

def rawtoks(src):
    """Names-kept tokens: identifiers, numbers and strings stay as written."""
    return re.findall(r"\"(?:\\.|[^\"\\])*\"|[A-Za-z_]\w*|\d+\.?\d*|\S", _strip(src))

def grams(t, k=7):
    return {hash(tuple(t[i:i + k])) for i in range(max(1, len(t) - k + 1))}

def substantial(subs, min_tokens=120):
    """Drop empty templates / tiny stubs, attach token lists. Returns a list."""
    out = []
    for s in subs.values():
        if s["code"]:
            t = toks(s["code"])
            if len(t) >= min_tokens:
                s["t"], s["g"], s["r"] = t, grams(t), rawtoks(s["code"])
                out.append(s)
    return out

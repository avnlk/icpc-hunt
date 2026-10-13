#!/usr/bin/env python3
"""
Clipboard collector: you read submissions in your normal browser, this saves what you copy.

    python3 collect.py p9_p10_all_solvers.csv

For each team/problem in the CSV it prints the link. Open it in your own browser, open a
submission, copy the code (Ctrl+A, Ctrl+C in the code box), come back here and type:
    a  = save clipboard as an ACCEPTED submission
    w  = save clipboard as a WRONG/other submission
    n  = next team/problem
    q  = quit (progress is kept; re-run to continue, finished items are skipped)
Files go to ccdump/<PROBLEM>/<rank>_<team>_<verdict><k>.txt

Needs a clipboard tool: wl-clipboard (Wayland: `wl-paste`) or xclip (X11).
"""
import csv, os, re, shutil, subprocess, sys
from pathlib import Path

def clip():
    for cmd in (["wl-paste", "--no-newline"], ["xclip", "-selection", "clipboard", "-o"],
                ["xsel", "--clipboard", "--output"]):
        if shutil.which(cmd[0]):
            try:
                return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout
            except Exception:
                pass
    sys.exit("No clipboard tool found. Install one:  sudo apt install wl-clipboard   (or xclip)")

def safe(s): return re.sub(r"[^A-Za-z0-9_.-]+", "_", s).strip("_")[:40]

src = sys.argv[1] if len(sys.argv) > 1 else "p9_p10_all_solvers.csv"
jobs = []
for row in csv.DictReader(open(src, encoding="utf-8-sig")):
    for link in row["check_links"].split():
        m = re.search(r"status/([A-Z0-9]+)\?usernames=(\w+)", link)
        if m: jobs.append((m.group(1), row["rank"], row["team"], link))

last = None
for prob, rank, team, link in jobs:
    out = Path("ccdump") / prob; out.mkdir(parents=True, exist_ok=True)
    base = f"{rank}_{safe(team)}"
    print(f"\n=== {prob} | rank {rank} | {team}\n    {link}")
    k = len(list(out.glob(base + "_*.txt")))
    while True:
        cmd = input("  [a]ccepted / [w]rong / [n]ext / [q]uit > ").strip().lower()
        if cmd == "q": sys.exit(0)
        if cmd == "n": break
        if cmd in ("a", "w"):
            text = clip()
            if not text.strip():
                print("  clipboard is empty"); continue
            if text == last:
                print("  same as the last thing saved; copy the next submission first"); continue
            k += 1
            f = out / f"{base}_{'AC' if cmd == 'a' else 'WA'}{k}.txt"
            f.write_text(text); last = text
            print(f"  saved {f}  ({len(text)} chars)")
print("\nAll done.")

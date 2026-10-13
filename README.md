# icpc-hunt

Community review of the **ICPC India 2026 Preliminary Contest** (CodeChef contest `ICPCOL2026`).

The organisers made every submission public for review and ask the community to report suspected
plagiarism through their form. This repo has tools to compare the published submissions, and a list of
submissions that looked worth a second pair of eyes. **Please verify before reporting anything.**

> **Not accusations.** Similar code can come from a short standard solution, a common template, or code
> generators. Everything here is "please check this", not a finding. Many early leads turned out to be a
> team's own earlier drafts (see *Checked and cleared* in `evidence/README.md`). Report through the official
> form only, and only teams that are still in the Selection Pool. Please be kind to the people involved.

## Start here

1. **[`evidence/README.md`](evidence/README.md)**: the submissions to check. Each row has a CodeChef link,
   the verdict, the team name (or *need to verify*), the username, and a copy of the code.
2. **How you can help** (below).
3. Or run the tools on your own downloads (see *Tools*).

## How you can help

- **Verify owners.** For each submission in `evidence/README.md`, open the link and read the "Submission by"
  line. If two submissions that look alike are by the **same** user, it is that team's own draft: tell us.
  If they differ, add the usernames and team names you find.
- **Fill in "need to verify".** Submissions by users no longer in the Selection Pool have no team name in the
  data files. If you know which team a username belongs to, say so.
- **Read the code.** Groups F and G in the evidence list were only scored, not read by hand.
- **Add data.** Only P8 (`IC26AM`) and P10 (`IC26BM`) have bulk data and P9 has just its solvers. Problem 7
  (`IC26TM`, ~150 solvers) is the best next one: the leaked booklet has distinctive lines for it
  (see `leak/FINGERPRINTS.md`). `p7_part1.csv` ... `p7_part6.csv` split its solvers into chunks of ~25.
- **Report** what holds up to the organisers' plagiarism form (linked from indiaicpc.in).

### Open questions

1. Is the idiom shape in group D (`precompute()` + `solve()` with `if(!(cin>>n)) return;`) common in generated
   code? If you can show it is, that group matters less.
2. Do the same excluded usernames recur across problems? (Group A's usernames, for example.)
3. Which pool teams in group F / G, once read, look like independent solutions?
4. Did last year's selection use an explicit solve cutoff? (See `docs/selection_rules.md`.)
5. Is the booklet in `leak/` authentic, and when was it handed out?

Open an Issue with the submission ids and what you found.

## Layout

| Path | What it is |
|---|---|
| `evidence/` | Submissions to check (links, team or *need to verify*, copies of the code), write-ups and match CSVs. |
| `analysis/` | Scripts that compare downloaded submissions. |
| `cc_dump.py` | Downloads submissions in a visible Chrome window; you complete any Cloudflare check by hand. |
| `collect.py` | Clipboard collector: copy code in your own browser, it saves it under the right name. |
| `autoclick.py` | Plain "click where the pointer is, once a second" helper (needs `ydotool` or `xdotool`). |
| `selection_pool_2026-10-12.csv` | The organisers' published Selection Pool (rank, username, team, college, per-problem scores). |
| `p7_part*.csv`, `p8_part*.csv`, `p9_p10_all_solvers.csv` | Teams that solved a problem, with status-page links, in chunks so several people can share the work. |
| `anomaly_review_list_v2.csv` | Teams that solved a hard problem (P7-P10) while skipping two or more problems that more teams solved. A reason to read their code, nothing more. |
| `leak/` | Typed-in solutions from an alleged coach-distributed booklet, plus grep patterns. |
| `docs/selection_rules.md` | The published regional selection rules, in plain terms. |
| `.github/workflows/fetch.yml` | Tried the downloader on GitHub Actions. **Does not work**: Cloudflare challenges GitHub's servers. Kept for reference. |

Problem codes: P1 `PHNCHRG`, P2 `IC26CS`, P3 `IC26MP`, P4 `IC26CB`, P5 `IC26SH`, P6 `IC26LR`, P7 `IC26TM`,
P8 `IC26AM`, P9 `IC26MM`, P10 `IC26BM`.
Status page: `https://www.codechef.com/ICPCOL2026/status/<CODE>` (add `?usernames=<id>` to filter).
One submission: `https://www.codechef.com/viewsolution/<id>`.

## Tools

### Setup (Linux)
```bash
python3 -m venv .venv
.venv/bin/pip install playwright
.venv/bin/python -m playwright install chromium     # only needed for cc_dump.py
```
The analysis scripts use only the standard library.

### Getting submissions
CodeChef puts a Cloudflare "verify you are human" check in front of the status pages. These tools **do not
try to get around it**: they stop and wait for you.

**`cc_dump.py`** opens a visible Chrome window and walks the status pages.
```bash
.venv/bin/python cc_dump.py --targets p9_p10_all_solvers.csv   # only the teams in the CSV's check_links column
.venv/bin/python cc_dump.py IC26MM IC26BM                      # whole problems
.venv/bin/python cc_dump.py --list-only IC26AM                 # submission lists only, no code
.venv/bin/python cc_dump.py --login --targets ...              # wait while you sign in by hand, then: touch ccdump/.go
```
- If the check appears, complete it yourself. The script resumes when it clears and stops if it does not
  clear within 15 minutes. Keep the window open until it prints "Done".
- Output: `ccdump/<CODE>/list.csv` and `ccdump/<CODE>/code/<id>.txt`. Existing code files are skipped, so you can resume.
- It waits about a second between pages.

**`collect.py`** is the fallback when downloading is blocked.
```bash
python3 collect.py p9_p10_all_solvers.csv
```
It prints each team's link; open it in your browser, copy a submission's code, and type `a` (accepted), `w` (wrong),
`n` (next) or `q` (quit). Files go to `ccdump/<CODE>/<rank>_<team>_<AC|WA><n>.txt`.
On Wayland install `wl-clipboard`.

**`autoclick.py`**: `python3 autoclick.py [--interval 1] [--count N] [--button left]`. Needs `ydotool` (Wayland;
run `sudo ydotoold --socket-perm=0666`, then `sudo chmod 666 /tmp/.ydotool_socket`) or `xdotool` (X11/XWayland
only). Stop with Ctrl+C.

### Analysing them
Run from the repo root. A submission whose username is not in the pool is **excluded** (withdrawn or removed
team; the published submissions include them, and they can be the *source* of a copy). Code files with no row in
`list.csv` are **unattributed**.
```bash
python3 analysis/similarity.py IC26BM 30                              # top 30 most similar cross-user pairs
python3 analysis/clusters.py IC26AM 0.88                              # connected groups, tagged pool/excluded
python3 analysis/matches_csv.py IC26AM evidence/P8_matches.csv 0.80   # every pair >= 0.80 -> CSV (+ by-team CSV)
python3 analysis/anomalies.py                                         # skip-pattern list -> anomaly_review_list_v2.csv
```
- Code under 120 tokens (empty templates, input-reading stubs) is ignored.
- **Scores:** *names ignored* replaces every variable name with a placeholder (structure only); *names kept* also
  needs identifiers, numbers and strings to match. 1.00 = identical.
- The same user twice is skipped. P8 is a ~15-line formula, so honest solutions score high there.

### Leaked booklet check
`leak/` has typed-in solutions from a booklet reportedly handed out by coaches, and `leak/FINGERPRINTS.md` has
grep patterns, for example
```bash
grep -rlE 'StringTokenizer st = new StringTokenizer\(""\)|class Solution[A-J]\b' ccdump/
```
No hits so far in the P8/P10 code collected (the booklet has no P8/P10 solution).

## Limits
- Scores measure similarity, not intent or direction; order is by submission id only.
- `list.csv` for P8 and P10 covers only part of the contest; code files without a row stay *unattributed*.
- Nothing here has been confirmed by the organisers.

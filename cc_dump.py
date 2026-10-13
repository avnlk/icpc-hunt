#!/usr/bin/env python3
"""
Download ICPC India 2026 prelim submissions from CodeChef (contest ICPCOL2026).

Setup (Linux):
    pip install playwright
    playwright install chromium

Run:
    python3 cc_dump.py --targets anomaly_review_list_v2.csv   # only flagged teams (fast, start here)
    python3 cc_dump.py                     # all 10 problems
    python3 cc_dump.py IC26MM IC26BM       # only some problems
    python3 cc_dump.py --list-only IC26AM  # only the submission lists, no code

Output:  ccdump/<PROBLEM>/list.csv       (id, user, time, verdict, lang, raw row text)
         ccdump/<PROBLEM>/code/<id>.txt  (source code)
         ccdump/<PROBLEM>/raw_json/*.json (every JSON the page loaded, for debugging)

A visible browser opens. If CodeChef asks you to log in, log in once in that window;
the profile is kept in ./cc_profile so later runs reuse it.
"""
import collections, csv, json, os, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

CONTEST = "ICPCOL2026"
PROBLEMS = ["PHNCHRG", "IC26CS", "IC26MP", "IC26CB", "IC26SH",
            "IC26LR", "IC26TM", "IC26AM", "IC26MM", "IC26BM"]
DELAY = 1.0          # seconds between page loads; be polite
MAX_PAGES = 2000

args = [a for a in sys.argv[1:] if not a.startswith("--")]
LIST_ONLY = "--list-only" in sys.argv
# --targets FILE.csv : only fetch the (problem, username) pairs in the check_links column
TARGETS = None
if "--targets" in sys.argv:
    tf = sys.argv[sys.argv.index("--targets") + 1]
    args = [a for a in args if a != tf]
    TARGETS = collections.defaultdict(list)
    for row in csv.DictReader(open(tf)):
        for link in row.get("check_links", "").split():
            m = re.search(r"status/([A-Z0-9]+)\?usernames=(\w+)", link)
            if m: TARGETS[m.group(1)].append(m.group(2))
probs = args or (sorted(TARGETS) if TARGETS else PROBLEMS)
OUT = Path("ccdump")

def note(msg):
    """Print, and surface as a GitHub annotation when running in Actions."""
    print(msg, flush=True)
    if os.environ.get("CI"):
        print("::warning::" + msg.replace("\n", " ")[:900], flush=True)

def challenged(page):
    """True while the page is Cloudflare's 'verify you are human' interstitial."""
    if page.is_closed():
        raise SystemExit("Browser window was closed. Re-run, and leave the window open until the script says Done.")
    try:
        t = page.title()
        b = page.evaluate("() => document.body ? document.body.innerText.slice(0, 300) : ''")
        return "Just a moment" in t or "security verification" in b
    except Exception:
        return False

def wait_for_human(page, timeout=900):
    """Do NOT touch the check. Just wait (up to `timeout` s) for the person at the
    keyboard to clear it in the visible browser window, then carry on."""
    if not challenged(page):
        return
    print("\n>>> Cloudflare check is showing in the browser window. "
          "Please complete it by hand; the script resumes automatically. <<<", flush=True)
    t0 = time.time()
    while challenged(page) and time.time() - t0 < timeout:
        time.sleep(2)
    if challenged(page):
        print(">>> still blocked after waiting; stopping without fetching submissions.", flush=True)
        raise SystemExit("Cloudflare verification was not cleared.")
    print(">>> check cleared, continuing.", flush=True)

def goto(page, url):
    if page.is_closed():
        raise SystemExit("Browser window was closed. Re-run, and leave the window open until the script says Done.")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if not os.environ.get("CI"):
            wait_for_human(page)
        try:
            page.wait_for_selector('a[href*="viewsolution"]', timeout=20000)
        except Exception:
            pass
        if challenged(page):
            if not os.environ.get("CI"):
                wait_for_human(page)
            if challenged(page):
                raise SystemExit("Cloudflare still blocks the status page; stopping.")
        return True
    except Exception as e:
        note(f"goto failed {url}: {type(e).__name__}: {e}")
        return False

def diag(page, tag):
    try:
        title = page.title()
        body = page.evaluate("() => document.body ? document.body.innerText.slice(0, 400) : ''")
        note(f"[{tag}] url={page.url} title={title!r} body={body!r}")
    except Exception as e:
        note(f"[{tag}] diag failed: {e}")

def scrape_rows(page):
    """Return list of dicts from the visible status table, plus solution ids from links."""
    return page.evaluate(r"""() => {
        const out = [];
        document.querySelectorAll('tr').forEach(tr => {
            const a = tr.querySelector('a[href*="viewsolution"]');
            if (!a) return;
            const m = a.getAttribute('href').match(/viewsolution\/(\d+)/);
            if (!m) return;
            const cells = [...tr.querySelectorAll('td')].map(td => td.innerText.trim());
            out.push({id: m[1], cells: cells});
        });
        return out;
    }""")

def fetch_code(page, sid):
    for url in (f"https://www.codechef.com/viewplaintext/{sid}",
                f"https://www.codechef.com/api/submission-details/{sid}"):
        try:
            r = page.request.get(url, timeout=30000)
            if r.status != 200:
                continue
            body = r.text()
            if url.endswith(sid) and "viewplaintext" in url:
                body = re.sub(r"^\s*<pre>|</pre>\s*$", "", body.strip())
                if body and "<html" not in body[:200].lower():
                    return body
            else:
                j = json.loads(body)
                d = j.get("data", j)
                for k in ("code", "solution", "source"):
                    if isinstance(d, dict) and d.get(k):
                        return d[k]
        except Exception:
            pass
    return None

with sync_playwright() as p:
    CI = bool(os.environ.get("CI"))
    ctx = p.chromium.launch_persistent_context(
        "cc_profile_chrome", channel="chrome", headless=CI, slow_mo=150
    )
    page = ctx.new_page()
    OUT.mkdir(exist_ok=True)
    if not CI and "--login" in sys.argv:
        # You sign in BY HAND in the browser window (your own account); the script never sees credentials.
        # When you are signed in, run:  touch ccdump/.go   (or ask Claude to) and it continues.
        go = OUT / ".go"; go.unlink(missing_ok=True)
        goto(page, "https://www.codechef.com/login")
        print("\n>>> Sign in to CodeChef in the browser window yourself. When done, run:  touch ccdump/.go  <<<", flush=True)
        t0 = time.time()
        while not go.exists() and time.time() - t0 < 1200:
            if page.is_closed():
                raise SystemExit("Browser window was closed. Re-run, and leave the window open until the script says Done.")
            time.sleep(2)
        print(">>> continuing." if go.exists() else ">>> no go-ahead after 20 min; stopping.", flush=True)
        if not go.exists():
            raise SystemExit("Login step timed out.")
    if not CI:
        # Open a real status page first so any check shows up now, while you are watching.
        first = probs[0] if probs else PROBLEMS[0]
        goto(page, f"https://www.codechef.com/{CONTEST}/status/{first}")
        diag(page, "first status page")

    for prob in probs:
        d = OUT / prob; (d / "code").mkdir(parents=True, exist_ok=True); (d / "raw_json").mkdir(exist_ok=True)
        jcount = [0]
        def on_resp(resp, d=d):
            try:
                if "application/json" in (resp.headers.get("content-type") or ""):
                    jcount[0] += 1
                    (d / "raw_json" / f"{jcount[0]:05d}.json").write_text(resp.text())
            except Exception:
                pass
        page.on("response", on_resp)

        seen, rows = set(), []
        queries = [f"usernames={u}&" for u in TARGETS[prob]] if TARGETS else [""]
        for qy in queries:
          for pg in range(MAX_PAGES):
            url = f"https://www.codechef.com/{CONTEST}/status/{prob}?{qy}page={pg}"
            goto(page, url)
            time.sleep(DELAY)
            got = scrape_rows(page)
            if pg == 0:
                diag(page, f"{prob} {qy}page0 rows={len(got)}")
                (d / f"page0_{qy.strip('&') or 'all'}.html").write_text(page.content())
            new = [g for g in got if g["id"] not in seen]
            if not new:
                break
            for g in new:
                g["query"] = qy.strip("&"); seen.add(g["id"]); rows.append(g)
            print(f"{prob} {qy}page {pg}: +{len(new)} (total {len(rows)})")
        page.remove_listener("response", on_resp)

        note(f"{prob}: {len(rows)} submissions listed")
        with open(d / "list.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["id", "query", "cells"])
            for g in rows: w.writerow([g["id"], g.get("query", ""), " | ".join(g["cells"])])

        if LIST_ONLY:
            continue
        for i, g in enumerate(rows, 1):
            fp = d / "code" / f"{g['id']}.txt"
            if fp.exists():
                continue
            code = fetch_code(page, g["id"])
            if code is None:
                goto(page, f"https://www.codechef.com/viewsolution/{g['id']}")
                code = page.evaluate("() => (document.querySelector('pre, .ace_content, code')||{}).innerText || ''")
            fp.write_text(code or "")
            if i == 1:
                note(f"{prob}: first code id={g['id']} len={len(code or '')} head={(code or '')[:120]!r}")
            if i % 50 == 0:
                print(f"{prob}: code {i}/{len(rows)}")
            time.sleep(DELAY / 2)
    ctx.close()
print("Done. Zip the ccdump folder and upload it.")

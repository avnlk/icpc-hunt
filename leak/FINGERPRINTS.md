# Leaked booklet ("ICPC India Online Round 2026 • Editorial Compendium") — fingerprints


Letter mapping (B = "Cyclic Shift" = IC26CS confirms A–J = P1–P10):
A PHNCHRG, B IC26CS, C IC26MP, D IC26CB, E IC26SH, F IC26LR, G IC26TM, H IC26AM, I IC26MM, J IC26BM.

## Caveat
Authenticity and timing are unverified. If the booklet was made AFTER submissions went public
(12 Oct evening), it could have been built from someone's public code — then a match proves nothing by itself.
Strong evidence = a team's code matches the booklet AND the team's own style elsewhere differs, or several
teams from unrelated colleges all match it.

## Grep patterns (use `grep -lE` over downloaded code)
Java template (all Java pages share it):
- `StringTokenizer st = new StringTokenizer\(""\)`
- `if \(line == null\) return;`
- `int t = Integer\.parseInt\(line\.trim\(\)\)`
- `while \(!st\.hasMoreTokens\(\)\) st = new StringTokenizer\(br\.readLine\(\)\)`
- `class Solution[A-J]\b`
C template:
- `if \(scanf\("%d", &t\) == 1\) while \(t--\) solve\(\)`
- `if \(scanf\("%lld %lld", &n, &m\) != 2\) return;`
- `\bcmp_ll\b|\bmin_ll\b|\bmax_ll\b`
Problem-specific:
- P3 (C): `L_min`, `R_min`, `// Option 1: prioritize L_min`, `cost1`, `cost2`
- P4 (D): `const int MAXW = 4005`, `bitset<MAXW>`, `min_w1 = max\(0, W - k\)`, `new BitSet\(4005\)`
- P7 (G): `// Reverse order`, `Math\.max\(6 \* x, Math\.max\(4 \* \(x \+ y\), 3 \* \(x \+ y \+ z\)\)\)`
- P9 (I): `System\.arraycopy\(nxt, 1, dp, 1, n - len \+ 1\)`, `nxt\[l\] = \(dp\[l \+ 1\] \+ dp\[l\]\) % MOD`
- P2 (B): `d\[i\] = abs\(a\[i\] - a\[\(i \+ 1\) % n\]\)` and `cout << d\[n - 2\]`

## Use in similarity runs
Put the matching file into each problem's JPlag/Dolos folder as submission `LEAK`.

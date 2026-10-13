# P8 (IC26AM): four pool teams sharing a rare code shape, in submission order

Pattern: `precompute()`/`pre()` + `solve()` split for a ten-line solution, with
`if(!(cin>>n)) return;` and/or `if(cin>>t){ while(t--) solve(); }`.
Across the 251 C/C++ submissions collected for P8, 7 contain `if(cin>>x)` or `if(!(cin>>x))`
(6 users; 4 pool teams). In P10, 0 pool teams use it.

| order (id) | team | rank | verdict | raw-text similarity to Recursive Raiders |
|---|---|---|---|---|
| [1368468730](https://www.codechef.com/viewsolution/1368468730) | Recursive Raiders | 554 | AC | (reference) |
| [1368475041](https://www.codechef.com/viewsolution/1368475041) | Graph Gurus | 96 | AC | 0.92 |
| [1368475384](https://www.codechef.com/viewsolution/1368475384) | Graph Gurus | 96 | AC | 0.92 |
| [1368476038](https://www.codechef.com/viewsolution/1368476038) | Runtime Hacker | 409 | WA | 0.81 |
| [1368476546](https://www.codechef.com/viewsolution/1368476546) | Bit Masker | 1031 | WA | 0.65 |

## Details
- **Graph Gurus vs Recursive Raiders:** identical set of identifiers (`precompute`, `solve`, `MAXN`, `inv`, `H`, `coef`, `ans`),
  same `if(!(cin>>n)) return;` and `if(cin>>t)` structure, same `ios::sync_with_stdio(false); cin.tie(nullptr);`.
  Only formatting differs, plus one edit: `H[i]=(H[i-1]+inv[i]%MOD)` vs `(H[i-1]+inv[i])%MOD`.
- **Runtime Hacker (WA):** same `precompute()`/`solve()`/`MAXI` shape; the code has typos (`cosnt int MAXI`, `H[I] = ...`).
- **Bit Masker (WA):** same skeleton (`pre()`, `solve()`, `if(!(cin>>n)) return;`) with macros; the `pre();` call is commented out.
- The two excluded users who also use the idiom (icpcol260943, icpcol263574) are only 0.23 and 0.39 similar to
  Recursive Raiders, so the idiom alone does not settle anything; what stands out is the shared skeleton and the order of submission.

## Caveats
- The formula is the standard one for P8; similarity of structure and the idiom can also come from generated code.
- Order is by submission id only; it does not show who copied from whom.

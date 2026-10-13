# Evidence: submissions to check

Each row is a CodeChef submission with a link and a copy of its code in [`code/`](code/). **Team name** is taken from the Selection Pool when the username is still in it; submissions by users who are no longer in the pool (withdrawn / excluded teams) have no team name in these files, so they say *need to verify*. Open the link and check the **Submission by** line.

This page lists what to look at. It is not a finding that anyone copied anything: similarity can also come from a standard solution, common templates, or generated code. Only teams still in the Selection Pool can be reported through the form.

| Problem | codes |
|---|---|
| P8 | IC26AM |
| P10 | IC26BM |


## A. P10: Python solutions with the same structure (Null Titans and four excluded users)

**What matched:** Seven Python 3 submissions to P10 with the same program shape: a one-line chained decrement `a-=l==0; b-=l==1; C-=l==2; d-=l==3`, input sliced as `d[1+4*i: 5+4*i]`, the answer built as `'0'*(...) + '01'*y + '1'*(...) + s`, and a running minimum `if best is None or res < best`. Variable names change between them (`be` -> `bestt` -> `besttt`). Of 111 other Python P10 submissions in the dump, none has both the decrement line and the slice. Earliest id is Null Titans'.

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368446624](https://www.codechef.com/viewsolution/1368446624) | AC | Null Titans (#1) | icpcol263329 | [P10_1368446624.txt](code/P10_1368446624.txt) |
| [1368458414](https://www.codechef.com/viewsolution/1368458414) | AC | need to verify | icpcol261170 | [P10_1368458414.txt](code/P10_1368458414.txt) |
| [1368458600](https://www.codechef.com/viewsolution/1368458600) | AC | need to verify | icpcol261170 | [P10_1368458600.txt](code/P10_1368458600.txt) |
| [1368468854](https://www.codechef.com/viewsolution/1368468854) | WA | need to verify | icpcol262403 | [P10_1368468854.txt](code/P10_1368468854.txt) |
| [1368469657](https://www.codechef.com/viewsolution/1368469657) | AC | need to verify | icpcol264518 | [P10_1368469657.txt](code/P10_1368469657.txt) |
| [1368469844](https://www.codechef.com/viewsolution/1368469844) | AC | need to verify | icpcol265366 | [P10_1368469844.txt](code/P10_1368469844.txt) |
| [1368470657](https://www.codechef.com/viewsolution/1368470657) | AC | need to verify | icpcol262403 | [P10_1368470657.txt](code/P10_1368470657.txt) |

## B. P10: CoreX and an excluded user (all wrong attempts)

**What matched:** Same brute force (`pop(i)`, `pop(j)`, `f(tuple(sorted(y)))`, `r=z if r is None or z<r else r`). CoreX's version has garbled text (`functoolsimportlru_cache`, `tuples`, `sorted9y`). Closest pair: 1368462543 and 1368456405 (0.94).

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368462543](https://www.codechef.com/viewsolution/1368462543) | WA | CoreX (#3052) | icpcol261595 | [P10_1368462543.txt](code/P10_1368462543.txt) |
| [1368455889](https://www.codechef.com/viewsolution/1368455889) | WA | need to verify | icpcol264215 | [P10_1368455889.txt](code/P10_1368455889.txt) |
| [1368455978](https://www.codechef.com/viewsolution/1368455978) | WA | need to verify | icpcol264215 | [P10_1368455978.txt](code/P10_1368455978.txt) |
| [1368456300](https://www.codechef.com/viewsolution/1368456300) | WA | need to verify | icpcol264215 | [P10_1368456300.txt](code/P10_1368456300.txt) |
| [1368456405](https://www.codechef.com/viewsolution/1368456405) | WA | need to verify | icpcol264215 | [P10_1368456405.txt](code/P10_1368456405.txt) |

## C. P10: Code Nova win and an excluded user (all wrong attempts)

**What matched:** Both build up to four candidate strings from `z=c00+c10`, `o=c01+c11` and print the `min`. Closest pair: 1368474166 and 1368454398 (0.98 names ignored, 0.73 raw text).

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368474166](https://www.codechef.com/viewsolution/1368474166) | WA | Code Nova win (#460) | icpcol261263 | [P10_1368474166.txt](code/P10_1368474166.txt) |
| [1368462878](https://www.codechef.com/viewsolution/1368462878) | WA | Code Nova win (#460) | icpcol261263 | [P10_1368462878.txt](code/P10_1368462878.txt) |
| [1368468852](https://www.codechef.com/viewsolution/1368468852) | WA | Code Nova win (#460) | icpcol261263 | [P10_1368468852.txt](code/P10_1368468852.txt) |
| [1368470239](https://www.codechef.com/viewsolution/1368470239) | WA | Code Nova win (#460) | icpcol261263 | [P10_1368470239.txt](code/P10_1368470239.txt) |
| [1368454398](https://www.codechef.com/viewsolution/1368454398) | WA | need to verify | icpcol264924 | [P10_1368454398.txt](code/P10_1368454398.txt) |

## D. P8: Four pool teams sharing a code shape

**What matched:** `precompute()` (or `pre()`) plus `solve()`, with `if(!(cin>>n)) return;` and/or `if(cin>>t){ while(t--) solve(); }`. In 251 collected C/C++ P8 submissions, 7 contain `if(cin>>x)` or `if(!(cin>>x))`; 4 are these pool teams. Two excluded users who also use the idiom are only 0.23 and 0.39 similar to Recursive Raiders. Raw-text similarity to Recursive Raiders: Graph Gurus 0.92, Runtime Hacker 0.81, Bit Masker 0.65.

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368468730](https://www.codechef.com/viewsolution/1368468730) | AC | Recursive Raiders (#554) | icpcol263751 | [P8_1368468730.txt](code/P8_1368468730.txt) |
| [1368475041](https://www.codechef.com/viewsolution/1368475041) | AC | Graph Gurus (#96) | icpcol262238 | [P8_1368475041.txt](code/P8_1368475041.txt) |
| [1368475384](https://www.codechef.com/viewsolution/1368475384) | AC | Graph Gurus (#96) | icpcol262238 | [P8_1368475384.txt](code/P8_1368475384.txt) |
| [1368476038](https://www.codechef.com/viewsolution/1368476038) | WA | Runtime Hacker (#409) | icpcol263830 | [P8_1368476038.txt](code/P8_1368476038.txt) |
| [1368476546](https://www.codechef.com/viewsolution/1368476546) | WA | Bit Masker (#1031) | icpcol260765 | [P8_1368476546.txt](code/P8_1368476546.txt) |

## E. P8: Cypher-X and an excluded user

**What matched:** Python, same shape (whole input read at once, `if not ...: return`, `solve()` with a `__main__` guard, `next(iterator)` reading, `MAXN = 200005`) with every variable renamed. The excluded submission has the modulus typed `9982244353`.

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368472216](https://www.codechef.com/viewsolution/1368472216) | AC | Cypher-X (#22) | icpcol261702 | [P8_1368472216.txt](code/P8_1368472216.txt) |
| [1368459104](https://www.codechef.com/viewsolution/1368459104) | WA | need to verify | icpcol264706 | [P8_1368459104.txt](code/P8_1368459104.txt) |

## F. P8: Pool-to-pool pairs (scores only, code not yet read by hand)

**What matched:** Logic Legends/Code Flux 0.97, Null Terminators/Achievers 0.94, 404NotFound/Runtime Hacker 0.88 (names kept).

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368473535](https://www.codechef.com/viewsolution/1368473535) | WA | Logic Legends (#2569) | icpcol262872 | [P8_1368473535.txt](code/P8_1368473535.txt) |
| [1368470265](https://www.codechef.com/viewsolution/1368470265) | AC | Code Flux (#1967) | icpcol261234 | [P8_1368470265.txt](code/P8_1368470265.txt) |
| [1368458076](https://www.codechef.com/viewsolution/1368458076) | AC | Null Terminators (#1123) | icpcol263325 | [P8_1368458076.txt](code/P8_1368458076.txt) |
| [1368450733](https://www.codechef.com/viewsolution/1368450733) | WA | Achievers (#1112) | icpcol260303 | [P8_1368450733.txt](code/P8_1368450733.txt) |
| [1368470069](https://www.codechef.com/viewsolution/1368470069) | AC | 404NotFound (#381) | icpcol260222 | [P8_1368470069.txt](code/P8_1368470069.txt) |

## G. P8: Byte Forge and an excluded user (both wrong, C)

**What matched:** 0.91 names kept, 0.99 names ignored. Code not yet read by hand.

| Submission | Verdict | Team (rank) | Username | Code |
|---|---|---|---|---|
| [1368475954](https://www.codechef.com/viewsolution/1368475954) | WA | Byte Forge (#2391) | icpcol260983 | [P8_1368475954.txt](code/P8_1368475954.txt) |
| [1368464825](https://www.codechef.com/viewsolution/1368464825) | WA | need to verify | icpcol264773 | [P8_1368464825.txt](code/P8_1368464825.txt) |

## Checked and cleared (same user)

These looked like matches but the earlier submission belongs to the same user, so each is a team's own earlier draft. Nothing to report.

| Team | Submissions |
|---|---|
| Expertease (#141, icpcol262052) | [1368437923](https://www.codechef.com/viewsolution/1368437923), [1368446211](https://www.codechef.com/viewsolution/1368446211) |
| Yukinomial (#1162) | [1368432739](https://www.codechef.com/viewsolution/1368432739), [1368465735](https://www.codechef.com/viewsolution/1368465735) |
| PBS (#1886) | [1368442652](https://www.codechef.com/viewsolution/1368442652), [1368444194](https://www.codechef.com/viewsolution/1368444194) |
| John Wick Tree (#573) | [1368436790](https://www.codechef.com/viewsolution/1368436790), [1368444596](https://www.codechef.com/viewsolution/1368444596) |
| CP (#3177) | [1368379088](https://www.codechef.com/viewsolution/1368379088), [1368475877](https://www.codechef.com/viewsolution/1368475877) |


## Other files here

- [`P10_python_cluster.md`](P10_python_cluster.md) and [`P8_precompute_solve_group.md`](P8_precompute_solve_group.md): write-ups of groups A and D.
- [`P8_matches.csv`](P8_matches.csv): all 1,599 cross-user P8 pairs scoring 0.80 or higher, both scores, ids and status.
- [`P8_matches_by_pool_team.csv`](P8_matches_by_pool_team.csv): each pool team's best P8 match.
- Regenerate with `analysis/matches_csv.py` (see the top-level README).

# P10 (IC26BM) — Python submissions with a shared structure

Submission ids rise with time. All are Python 3.

| id | verdict | username | team (pool) | rank | college |
|---|---|---|---|---|---|
| [1368446624](https://www.codechef.com/viewsolution/1368446624) | AC | icpcol263329 | Null Titans | 1 | Padmashri Dr.B V Raju Institute Of Technology |
| [1368458414](https://www.codechef.com/viewsolution/1368458414) | AC | icpcol261170 | not in Selection Pool | - | - |
| [1368458600](https://www.codechef.com/viewsolution/1368458600) | AC | icpcol261170 | not in Selection Pool | - | - |
| [1368468854](https://www.codechef.com/viewsolution/1368468854) | WA | icpcol262403 | not in Selection Pool | - | - |
| [1368469657](https://www.codechef.com/viewsolution/1368469657) | AC | icpcol264518 | not in Selection Pool | - | - |
| [1368469844](https://www.codechef.com/viewsolution/1368469844) | AC | icpcol265366 | not in Selection Pool | - | - |
| [1368470657](https://www.codechef.com/viewsolution/1368470657) | AC | icpcol262403 | not in Selection Pool | - | - |

## Shared quirks (same in all 7)
- one-line chained decrement via boolean compare: `a-=l==0; b-=l==1; C-=l==2; d-=l==3`
- input sliced as `d[1+4*i: 5+4*i]` inside a generator passed to print/join
- building the answer as `'0'*(a+C+x) + '01'*y + '1'*(b+d-x-2*y) + s`
- running minimum via `if best is None or res < best`
- `# cook your dish here` default header kept

## Names change between the submissions (in order of id)
- Null Titans: `be`, `ans`, `s1`, `dt`, `w x y z`
- [1368458414](https://www.codechef.com/viewsolution/1368458414): `bestt`, `res`, `solve`, `d`, `a b C d`
- [1368470657](https://www.codechef.com/viewsolution/1368470657): `besttt`, `res`, `solve`, `d`, `a b C d`  (one more 't' than the previous)

## Contrast
Other Python P10 submissions in the dump: 111; with BOTH the chained-decrement line and the slice pattern: 0.
BitMasters (#6) and ICONIX (#8) wrote Python for the same problem with different structure.

## Caveats
- The algorithm (try each last block, then zeros, '01' repeats, ones) is the standard approach; many teams used it in C++ with different formulas.
- Only Null Titans is in the Selection Pool; the other users are not in the pool (withdrawn/excluded).
- Direction is by submission id only: Null Titans' accepted solution is the earliest. It does not show who copied from whom, or that the source wasn't a third party.

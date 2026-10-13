# Downloaded submissions

Copies of public CodeChef submissions to the ICPC India 2026 preliminary contest (`ICPCOL2026`), which the
organisers published for community review. Included so reviewers do not have to download them again.

**Permission and ownership.** The repo owner reports that the organisers agreed to these copies being shared among
reviewers for this purpose. The code belongs to the teams that wrote it (CodeChef's Terms, section 11); it is shared
here only for plagiarism review. Please do not reuse it for anything else, and do not re-upload it elsewhere.

| Path | Contents |
|---|---|
| `IC26AM/` (P8) | `list.csv` and `code/<id>.txt` for 419 submissions |
| `IC26BM/` (P10) | `list.csv` and `code/<id>.txt` for 557 submissions |

Only P8 and P10 are included. There is no data for the other problems.

- `list.csv` columns: `id`, `status_page` (the page it was read from), `cells` (id | age | result glyph, then
  username | points | runtime | memory | language). "(100)" in the points field means accepted.
- Usernames are the contest's own ids (`icpcolNNNNNN`), the same ones the organisers' reporting form asks for. Map them
  to teams with `selection_pool_2026-10-12.csv`; usernames missing from it belong to withdrawn or excluded teams.
- **Incomplete.** `list.csv` only covers part of the contest. Code files with no row in it (the earlier submissions)
  are *unattributed*: the code is there but the username is not. Check the "Submission by" line on CodeChef.
- Each file is the code as shown on CodeChef; wrong and accepted submissions are both included.
- Everyone's submissions are included as downloaded, with nothing added or removed.
- The analysis scripts read `ccdump/` if it exists (your own fresh download), otherwise this folder.

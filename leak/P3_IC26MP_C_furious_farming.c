/* LEAK booklet page 7/9 — "Problem C (Continued: C & Java Implementations)" (C). */
#include <stdio.h>
#include <stdlib.h>

int cmp_ll(const void *a, const void *b) {
    long long va = *(long long*)a, vb = *(long long*)b;
    return (va > vb) - (va < vb);
}
long long min_ll(long long a, long long b) { return a < b ? a : b; }
long long max_ll(long long a, long long b) { return a > b ? a : b; }

void solve(void) {
    long long n, m;
    if (scanf("%lld %lld", &n, &m) != 2) return;
    long long *x = (long long*)malloc(sizeof(long long) * m);
    for (int i = 0; i < m; i++) scanf("%lld", &x[i]);
    qsort(x, m, sizeof(long long), cmp_ll);
    long long L_min = x[0] - 1, R_min = n - x[m - 1], gap = 0;
    for (int i = 0; i < m - 1; i++) gap = max_ll(gap, x[i + 1] - x[i] - 1);
    long long L1 = L_min, R1 = max_ll(R_min, gap - L1);
    long long c1 = L1 + R1 + min_ll(L1, R1);
    long long R2 = R_min, L2 = max_ll(L_min, gap - R2);
    long long c2 = L2 + R2 + min_ll(L2, R2);
    printf("%lld\n", min_ll(c1, c2));
    free(x);
}

int main(void) {
    int t;
    if (scanf("%d", &t) == 1) while (t--) solve();
    return 0;
}

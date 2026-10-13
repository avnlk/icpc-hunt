// LEAK booklet page 8/9 — "Problem C: Furious Farming" (C++).
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void solve() {
    long long n, m;
    cin >> n >> m;
    vector<long long> x(m);
    for (int i = 0; i < m; i++) cin >> x[i];
    sort(x.begin(), x.end());
    long long L_min = x[0] - 1;
    long long R_min = n - x[m - 1];
    long long gap = 0;
    for (int i = 0; i < m - 1; i++) gap = max(gap, x[i + 1] - x[i] - 1);

    long long cost1 = 0, cost2 = 0;
    // Option 1: prioritize L_min
    long long L1 = L_min, R1 = max(R_min, gap - L1);
    cost1 = L1 + R1 + min(L1, R1);
    // Option 2: prioritize R_min
    long long R2 = R_min, L2 = max(L_min, gap - R2);
    cost2 = L2 + R2 + min(L2, R2);
    cout << min(cost1, cost2) << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    // [rest not visible]
}

// LEAK booklet page 9/9 — "Problem B: Cyclic Shift" (C++). Transcribed from photo; [?] = unreadable.
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;

void solve() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<long long> d(n);
    for (int i = 0; i < n; i++) d[i] = abs(a[i] - a[(i + 1) % n]);
    sort(d.begin(), d.end());
    cout << d[n - 2] << "\n";
}
// main() not visible

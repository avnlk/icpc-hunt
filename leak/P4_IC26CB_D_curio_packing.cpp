// LEAK booklet page 6/9 — "Problem D: Curio Packing" (C++). Truncated at bottom of photo.
// Editorial text: "Time-Reversal Dynamic Programming ... Process in reverse from n down to 1 ... maintains all valid w1 reachable values in <= 4000 states."
#include <iostream>
#include <string>
#include <bitset>
using namespace std;

const int MAXW = 4005;

void solve() {
    int n, k;
    cin >> n >> k;
    string s;
    cin >> s;
    bitset<MAXW> dp;
    dp.set(0);
    int W = 0;
    for (int i = n - 1; i >= 0; i--) {
        bitset<MAXW> nxt;
        int wt = (s[i] == 'G' ? 1 : 2);
        if (s[i] == 'G') {
            for (int w1 = 0; w1 <= min(W, k); w1++) {
                if (dp.test(w1)) nxt.set(w1 + 1);
            }
            int min_w1 = max(0, W - k);
            // [rest not visible]

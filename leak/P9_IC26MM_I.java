// LEAK booklet page 1/9 — Problem I (Java).  P9 = IC26MM, only 7 solvers nationally.
import java.io.*;
import java.util.*;

public class SolutionI {
    static final int MOD = 998244353;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer("");
        String line = br.readLine();
        if (line == null) return;
        int t = Integer.parseInt(line.trim());
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            for (int i = 0; i < n; i++) {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
                st.nextToken();
            }
            int[] dp = new int[n + 2];
            int[] nxt = new int[n + 2];
            for (int i = 1; i <= n; i++) dp[i] = 1;
            for (int len = 2; len <= n; len++) {
                for (int l = 1; l <= n - len + 1; l++) {
                    nxt[l] = (dp[l + 1] + dp[l]) % MOD;
                }
                System.arraycopy(nxt, 1, dp, 1, n - len + 1);
            }
            sb.append(dp[1]).append("\n");
        }
        System.out.print(sb);
    }
}

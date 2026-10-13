// LEAK booklet page 3/9 — Problem G (Java).
import java.io.*;
import java.util.*;

public class SolutionG {
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
            long[] a = new long[3 * n];
            for (int i = 0; i < 3 * n; i++) {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
                a[i] = Long.parseLong(st.nextToken());
            }
            Arrays.sort(a);
            // Reverse order
            for (int i = 0; i < (3 * n) / 2; i++) {
                long tmp = a[i]; a[i] = a[3 * n - 1 - i]; a[3 * n - 1 - i] = tmp;
            }
            long total = 0;
            for (int i = 0; i < n; i++) {
                long x = a[i];
                long y = a[2 * n - 1 - i];
                long z = a[2 * n + i];
                total += Math.max(6 * x, Math.max(4 * (x + y), 3 * (x + y + z)));
            }
            sb.append(total).append("\n");
        }
        System.out.print(sb);
    }
}

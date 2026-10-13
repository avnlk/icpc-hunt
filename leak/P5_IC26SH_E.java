// LEAK booklet page 4/9 — Problem E (Java). Truncated.
import java.io.*;
import java.util.*;

public class SolutionE {
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
            long c = Long.parseLong(st.nextToken());
            int[] p = new int[n];
            for (int i = 0; i < n; i++) {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
                p[i] = Integer.parseInt(st.nextToken()) - 1;
            }
            long[] a = new long[n];
            for (int i = 0; i < n; i++) {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
                a[i] = Long.parseLong(st.nextToken());
            }
            boolean[] vis = new boolean[n];
            long total = 0;
            for (int i = 0; i < n; i++) {
                if (vis[i]) continue;
                int curr = i;
                long sum = 0;
                int L = 0;
                // ArrayList<Long> gain = new ArrayList<>(); [partially visible]
                // [rest not visible]

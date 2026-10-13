// LEAK booklet page 5/9 — Problem D (Java). Truncated.
import java.io.*;
import java.util.*;

public class SolutionD {
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
            int k = Integer.parseInt(st.nextToken());
            while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
            String s = st.nextToken();
            BitSet dp = new BitSet(4005);
            dp.set(0);
            int W = 0;
            boolean ok = true;
            for (int i = n - 1; i >= 0; i--) {
                BitSet nxt = new BitSet(4005);
                char ch = s.charAt(i);
                int wt = (ch == 'G' ? 1 : 2);
                if (ch == 'G') {
                    for (int w1 = 0; w1 <= Math.min(W, k); w1++) {
                        if (dp.get(w1)) nxt.set(w1 + 1);
                        // [rest not visible]

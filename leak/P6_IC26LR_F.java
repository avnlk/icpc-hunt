// LEAK booklet page 2/9 — Problem F (Java). Truncated.
import java.io.*;
import java.util.*;

public class SolutionF {
    static class Point implements Comparable<Point> {
        long x, y;
        int orig;
        Point(long x, long y, int orig) { this.x = x; this.y = y; this.orig = orig; }
        public int compareTo(Point o) { return Long.compare(this.x, o.x); }
    }

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
            Point[] pts = new Point[n];
            for (int i = 0; i < n; i++) {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
                pts[i] = new Point(Long.parseLong(st.nextToken()), Long.parseLong(st.nextToken()), i);
            }
            Arrays.sort(pts);
            Integer[] order = new Integer[n];
            for (int i = 0; i < n; i++) order[i] = i;
            Arrays.sort(order, (a, b) -> Long.compare(pts[a].y, pts[b].y));
            int[] y = new int[n];
            for (int r = 0; r < n; r++) y[order[r]] = r + 1;
            int[] tails = new int[n];
            int tsz = 0;
            for (int i = 0; i < n; i++) {
                int v = -y[i];
                int lo = 0, hi = tsz;
                while (lo < hi) {
                    int mid = (lo + hi) >> 1;
                    if (tails[mid] >= v) hi = mid; // [rest not visible]

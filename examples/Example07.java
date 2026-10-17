import java.util.Arrays;

public class Example07 {
    public static void main(String[] args) {
        int[] heights = {3, 7, 2};
        int[] alias = heights;
        int[] copy = Arrays.copyOf(heights, heights.length);
        alias[0] = 9;
        System.out.println(Arrays.toString(heights));
        System.out.println(Arrays.toString(copy));
        int sum = 0;
        for (int value : heights) {
            sum += value;
        }
        System.out.println(sum);
    }
}

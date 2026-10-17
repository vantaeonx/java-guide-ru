public class Example06 {
    public static void main(String[] args) {
        int total = 0;
        for (int day = 1; day <= 4; day++) {
            total += day * 3;
        }
        System.out.println(total);
        int remaining = 3;
        while (remaining > 0) {
            System.out.print(remaining + " ");
            remaining--;
        }
        System.out.println("готово");
    }
}

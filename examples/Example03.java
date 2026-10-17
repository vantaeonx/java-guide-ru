public class Example03 {
    public static void main(String[] args) {
        int minutes = 95;
        System.out.println(minutes / 60 + ":" + minutes % 60);
        System.out.println(9 / 4);
        System.out.println(9 / 4.0);
        System.out.println(-9 % 4);
        boolean safe = minutes > 0 && 120 / minutes >= 1;
        System.out.println(safe);
    }
}

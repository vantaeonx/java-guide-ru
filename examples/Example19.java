public class Example19 {
    static int clamp(int value, int low, int high) {
        if (low > high) {
            throw new IllegalArgumentException("invalid bounds");
        }
        return Math.max(low, Math.min(value, high));
    }

    static void check(boolean condition, String name) {
        if (!condition) {
            throw new AssertionError(name);
        }
    }

    public static void main(String[] args) {
        check(clamp(-3, 0, 9) == 0, "below");
        check(clamp(4, 0, 9) == 4, "inside");
        check(clamp(12, 0, 9) == 9, "above");
        System.out.println("3 проверки пройдены");
    }
}

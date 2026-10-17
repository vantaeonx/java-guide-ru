public class Example14 {
    static int readCount(String text) {
        int value = Integer.parseInt(text);
        if (value < 0) {
            throw new IllegalArgumentException("negative count");
        }
        return value;
    }

    public static void main(String[] args) {
        String text = "many";
        try {
            System.out.println(readCount(text));
        } catch (IllegalArgumentException error) {
            System.out.println("Некорректное количество");
        }
        System.out.println("Программа продолжилась");
    }
}

public class Example17 {
    static final class Slot<T> {
        private final T value;

        Slot(T value) {
            this.value = value;
        }

        T get() {
            return value;
        }
    }

    static <T> T chooseFirst(T first, T second) {
        return first;
    }

    public static void main(String[] args) {
        Slot<String> slot = new Slot<>("карта");
        String item = slot.get();
        System.out.println(item);
        System.out.println(chooseFirst(6, 9));
    }
}

public class Example11 {
    static final class Charge {
        private final int capacity;
        private int amount;

        Charge(int capacity) {
            if (capacity <= 0) {
                throw new IllegalArgumentException("capacity must be positive");
            }
            this.capacity = capacity;
        }

        void add(int units) {
            if (units < 0 || units > capacity - amount) {
                throw new IllegalArgumentException("invalid charge");
            }
            amount += units;
        }

        int amount() {
            return amount;
        }
    }

    public static void main(String[] args) {
        Charge charge = new Charge(10);
        charge.add(4);
        System.out.println(charge.amount());
    }
}

public class Example10 {
    static class Beacon {
        int level;

        void raise() {
            level++;
        }
    }

    public static void main(String[] args) {
        Beacon north = new Beacon();
        Beacon alias = north;
        Beacon south = new Beacon();
        alias.raise();
        System.out.println(north.level);
        System.out.println(south.level);
        System.out.println(north == alias);
        System.out.println(north == south);
    }
}

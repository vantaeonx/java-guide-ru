public class Example12 {
    static abstract class Route {
        abstract int minutes();
    }

    static class Walk extends Route {
        @Override
        int minutes() {
            return 18;
        }
    }

    static class Tram extends Route {
        @Override
        int minutes() {
            return 7;
        }
    }

    public static void main(String[] args) {
        Route[] routes = {new Walk(), new Tram()};
        for (Route route : routes) {
            System.out.println(route.minutes());
        }
    }
}

public class Example13 {
    interface Output {
        void write(String message);
    }

    static class ConsoleOutput implements Output {
        @Override
        public void write(String message) {
            System.out.println(message);
        }
    }

    static class Greeting {
        private final Output output;

        Greeting(Output output) {
            this.output = output;
        }

        void welcome(String place) {
            output.write("Добро пожаловать: " + place);
        }
    }

    public static void main(String[] args) {
        Greeting greeting = new Greeting(new ConsoleOutput());
        greeting.welcome("мастерская");
    }
}

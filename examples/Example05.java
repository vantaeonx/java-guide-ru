public class Example05 {
    public static void main(String[] args) {
        int battery = 37;
        String state;
        if (battery < 0 || battery > 100) {
            state = "Некорректно";
        } else if (battery < 20) {
            state = "Зарядить";
        } else {
            state = "Можно ехать";
        }
        System.out.println(state);
    }
}

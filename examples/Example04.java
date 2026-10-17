import java.util.Scanner;

public class Example04 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String city = input.nextLine();
        int platforms = Integer.parseInt(input.nextLine().trim());
        System.out.println(city + ": " + (platforms + 1));
    }
}

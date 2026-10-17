import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Example15 {
    public static void main(String[] args) {
        List<String> stops = new ArrayList<>();
        stops.add("порт");
        stops.add("парк");
        stops.add("порт");
        Set<String> unique = new LinkedHashSet<>(stops);
        System.out.println(stops.size());
        System.out.println(unique);
        List<Integer> levels = new ArrayList<>(List.of(4, 8, 4));
        levels.remove(Integer.valueOf(4));
        System.out.println(levels);
    }
}

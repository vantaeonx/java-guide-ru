import java.util.LinkedHashMap;
import java.util.Map;

public class Example16 {
    public static void main(String[] args) {
        String[] tools = {"пила", "молоток", "пила"};
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String tool : tools) {
            int old = counts.getOrDefault(tool, 0);
            counts.put(tool, old + 1);
        }
        for (Map.Entry<String, Integer> entry : counts.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}

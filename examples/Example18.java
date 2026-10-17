import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Example18 {
    public static void main(String[] args) throws IOException {
        Path directory = Files.createTempDirectory("java-guide-");
        Path file = directory.resolve("routes.txt");
        try {
            Files.write(file, List.of("порт;12", "парк;5"),
                    StandardCharsets.UTF_8);
            List<String> lines = Files.readAllLines(file,
                    StandardCharsets.UTF_8);
            System.out.println(lines.size());
            System.out.println(lines.get(0));
        } finally {
            Files.deleteIfExists(file);
            Files.deleteIfExists(directory);
        }
    }
}

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Example20 {
    enum Priority { LOW, HIGH }

    record Ticket(String title, Priority priority) {
        Ticket {
            if (title == null || title.isBlank() || priority == null) {
                throw new IllegalArgumentException("invalid ticket");
            }
        }
    }

    public static void main(String[] args) {
        List<Ticket> tickets = new ArrayList<>(List.of(
                new Ticket("Мост", Priority.HIGH),
                new Ticket("Арка", Priority.LOW)));
        tickets.sort(Comparator.comparing(Ticket::title));
        tickets.forEach(ticket -> System.out.println(ticket.title()));
    }
}

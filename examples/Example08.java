import java.util.Locale;

public class Example08 {
    public static void main(String[] args) {
        String label = "  Dock-12  ";
        String clean = label.trim().toLowerCase(Locale.ROOT);
        System.out.println(clean);
        System.out.println(label.length());
        System.out.println(clean.substring(0, 4));
        String face = "\uD83D\uDE00";
        System.out.println(face.length());
        System.out.println(face.codePointCount(0, face.length()));
    }
}

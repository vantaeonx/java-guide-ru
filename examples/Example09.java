public class Example09 {
    static int perimeter(int width, int height) {
        return 2 * (width + height);
    }

    static void repaint(int[] cells) {
        cells[0] = 8;
        cells = new int[] {1, 1};
    }

    public static void main(String[] args) {
        int[] board = {2, 3};
        repaint(board);
        System.out.println(board[0]);
        int border = perimeter(4, 6);
        System.out.println(border);
    }
}

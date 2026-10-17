package ru.vantaeonx.javaguide.ch09;

// Автор: ____________________
// Ex080. Парсер и вычислитель
// Глава 09. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex080 {
    // Опора: Разделение чтения и вычисления позволяет проверить каждый этап отдельно.

    // Условие: Напиши static int parseMinutes(String text) для корректной целой строки с
    // краевыми пробелами и static long seconds(int minutes) для неотрицательного int. Main
    // применяет оба к text, печатает секунды. Обработку ошибочных строк пока не делай.

    static int parseMinutes(String text) {
        throw new UnsupportedOperationException("TODO");
    }
    static long seconds(int minutes) {
        throw new UnsupportedOperationException("TODO");
    }

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        String text = " 125 ";

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // 125 -> 7500; 0 -> 0.
        // 2147483647 -> 128849018820; методы ничего не читают из консоли.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

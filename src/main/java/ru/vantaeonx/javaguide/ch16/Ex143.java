package ru.vantaeonx.javaguide.ch16;

import java.util.LinkedHashMap;
import java.util.Map;

// Автор: ____________________
// Ex143. Слияние остатков
// Глава 16. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex143 {
    // Опора: Объединение карт требует отдельного правила для совпавших ключей.

    // Условие: Объедини left и right в новую LinkedHashMap<String,Long>, суммируя значения
    // общих ключей. Порядок: ключи left, затем новые из right. Исходники неизменны,
    // переполнение long исключено.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        Map<String, Long> left = new LinkedHashMap<>();
        left.put("A", 4L); left.put("B", 2L);
        Map<String, Long> right = new LinkedHashMap<>();
        right.put("B", 7L); right.put("C", 1L);

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Результат A=4,B=9,C=1.
        // Две пустые -> пустая; результат не является left или right.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

package ru.vantaeonx.javaguide.ch16;

import java.util.LinkedHashMap;
import java.util.Map;

// Автор: ____________________
// Ex137. Повторный put
// Глава 16. Уровень 1. Формат: Предсказать результат
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex137 {
    // Опора: Замена значения не добавляет второй экземпляр ключа.

    // Условие: Предскажи прежнее значение, размер и карту.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        Map<String, Integer> values = new LinkedHashMap<>();
        values.put("A", 2);
        Integer old = values.put("A", 7);
        values.put("B", 7);
        System.out.println(old);
        System.out.println(values.size());
        System.out.println(values);

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Прогноз до запуска.
        // Объяснено, почему одинаковые значения у разных ключей разрешены.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

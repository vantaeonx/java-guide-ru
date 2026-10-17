package ru.vantaeonx.javaguide.ch15;

import java.util.ArrayList;
import java.util.List;

// Автор: ____________________
// Ex128. Remove выбирает перегрузку
// Глава 15. Уровень 1. Формат: Предсказать результат
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex128 {
    // Опора: Int-аргумент может обозначать индекс, а Integer - значение.

    // Условие: Предскажи списки после каждой операции, объясни различие перегрузок.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        List<Integer> values = new ArrayList<>(List.of(5, 1, 5, 9));
        values.remove(1);
        System.out.println(values);
        values.remove(Integer.valueOf(5));
        System.out.println(values);

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Прогноз до запуска.
        // Указано, удаляется ли первое или любое вхождение значения.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

package ru.vantaeonx.javaguide.ch10;

// Автор: ____________________
// Ex083. Объект общий
// Глава 10. Уровень 1. Формат: Предсказать результат
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex083 {
    // Опора: Alias обозначает ещё один путь к уже созданному объекту.

    // Условие: Предскажи значения a.value, b.value, c.value и результаты ==.

    static class Cell { int value; }

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        Cell a = new Cell();
        a.value = 3;
        Cell b = a;
        Cell c = new Cell();
        c.value = 3;
        b.value = 8;
        System.out.println(a.value + "," + b.value + "," + c.value);
        System.out.println(a == b);
        System.out.println(a == c);

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Сначала прогноз.
        // Нарисованы два объекта и три ссылки.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

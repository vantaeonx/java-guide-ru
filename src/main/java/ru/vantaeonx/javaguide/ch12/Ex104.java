package ru.vantaeonx.javaguide.ch12;

// Автор: ____________________
// Ex104. Поля не полиморфны
// Глава 12. Уровень 2. Формат: Объяснить поведение
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex104 {
    // Опора: Динамический выбор относится к переопределённым методам экземпляра.

    // Условие: Предскажи два вывода и объясни, почему поле и метод могут показывать разные
    // значения.

    static class Parent {
        String label = "parent";
        String label() { return label; }
    }
    static class Kid extends Parent {
        String label = "kid";
        @Override String label() { return label; }
    }

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        Parent value = new Kid();
        System.out.println(value.label);
        System.out.println(value.label());

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Прогноз до запуска.
        // Различены скрытие поля и переопределение метода.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

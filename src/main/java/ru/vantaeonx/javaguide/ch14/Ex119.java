package ru.vantaeonx.javaguide.ch14;

// Автор: ____________________
// Ex119. Путь после отказа
// Глава 14. Уровень 1. Формат: Предсказать результат
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex119 {
    // Опора: После throw выполнение тела try не продолжается с места ошибки.

    // Условие: Предскажи порядок строк.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        try {
            System.out.println("A");
            Integer.parseInt("x");
            System.out.println("B");
        } catch (NumberFormatException error) {
            System.out.println("C");
        } finally {
            System.out.println("D");
        }
        System.out.println("E");

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Прогноз до запуска.
        // Указано, какая строка недостижима на этом входе.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

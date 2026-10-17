package ru.vantaeonx.javaguide.ch14;

// Автор: ____________________
// Ex124. Номер строки в отказе
// Глава 14. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex124 {
    // Опора: Полезное исключение сохраняет причину и контекст.

    // Условие: Создай ParseFailure extends Exception с конструктором (String message,
    // Throwable cause). Метод parse(String text,int line) преобразует int, а
    // NumberFormatException оборачивает в ParseFailure с номером строки. Main обрабатывает
    // ParseFailure.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        String text = "oops";
        int line = 7;

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Сообщение содержит 7, getCause() имеет тип NumberFormatException.
        // "12",7 -> 12; исходный cause не потерян.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

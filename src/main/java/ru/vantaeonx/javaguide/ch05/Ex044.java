package ru.vantaeonx.javaguide.ch05;

// Автор: ____________________
// Ex044. Приоритет доступа
// Глава 05. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex044 {
    // Опора: Сначала решается запрет, затем дополнительные возможности.

    // Условие: Выведи DENIED, если blocked или !authenticated. Иначе ADMIN для admin, EDIT
    // для editor, READ для остальных. Одновременно admin и editor -> ADMIN.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        boolean blocked = false;
        boolean authenticated = true;
        boolean admin = true;
        boolean editor = true;

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Исходный -> ADMIN.
        // Blocked запрещает даже admin; неавторизованный editor -> DENIED.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

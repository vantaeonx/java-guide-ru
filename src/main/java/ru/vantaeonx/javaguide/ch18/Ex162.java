package ru.vantaeonx.javaguide.ch18;

import java.util.List;

// Автор: ____________________
// Ex162. Сначала подготовить затем заменить
// Глава 18. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex162 {
    // Опора: Сохранение не должно уничтожать прежний файл на этапе подготовки.

    // Условие: Спроектируй и реализуй save(Path target,List<String> lines): temp-файл в
    // родительском каталоге, UTF-8 запись, move с ATOMIC_MOVE и REPLACE_EXISTING; если
    // AtomicMoveNotSupportedException, явно сообщи отказ и оставь старый target, без
    // тихого неатомарного fallback. В finally убери temp. Проверяй только свой sandbox.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        List<String> oldLines = List.of("OLD");
        List<String> newLines = List.of("NEW", "READY");

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // При успехе target содержит новые строки.
        // До move целевой файл не обрезается; неподдержанный atomic move имеет отдельную
        // политику; не обещана защита от всех аппаратных сбоев.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

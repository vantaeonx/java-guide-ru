package ru.vantaeonx.javaguide.ch11;

// Автор: ____________________
// Ex098. Перевод между резервуарами
// Глава 11. Уровень 3. Формат: Написать код
// Условие и проверки синхронизируются с course/catalog.json.
public class Ex098 {
    // Опора: Связанная операция должна проверить оба объекта до любых изменений.

    // Условие: Создай Tank с private capacity,amount, constructor(capacity,amount),
    // amount(). Напиши transferTo(Tank other,int units): units>=0, хватает источника и
    // места назначения; при отказе IllegalArgumentException, оба состояния прежние.
    // Перевод самому себе - отсутствие изменения при units<=amount.

    public static void main(String[] args) {
        // Исходные данные / исходный код для прогноза:
        int sourceCapacity = 10;
        int sourceAmount = 7;
        int targetCapacity = 8;
        int targetAmount = 2;

        // TODO: твой код. Для методов дополни тело и вызови их здесь.
        // Ответ / прогноз / объяснение: ____________________
        // Проверки своего решения:
        // Перевод 3 -> источник 4, цель 5.
        // Перевод 9 отвергнут без изменений; нулевой допустим; constructor требует
        // 0<=amount<=capacity.
    }

    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).
}

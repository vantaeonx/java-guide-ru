package ru.vantaeonx.javaguide.projects;


// Автор: ____________________
// Project04. Каталог мастерской
public class Project04 {
    // Создай Item с final id,name и private nonnegative int stock. Id/name непустые после
    // trim, id не меняется. Catalog хранит LinkedHashMap<String,Item>. Register запрещает
    // повтор id, increase(id,n) и take(id,n) требуют n>=0, take не превышает stock;
    // неизвестный id -> IllegalArgumentException. Увеличение, выходящее за int, запрещено
    // до изменения. History - List<String> только успешных операций с точным форматом
    // REGISTER:id, INCREASE:id:n, TAKE:id:n. List выдаётся неизменяемой копией.
    // LowStock(limit) возвращает id с stock<=limit в порядке регистрации, limit>=0. Main
    // работает с фиксированными операциями и проверками, без чтения файла.

    public static void main(String[] args) {
        // Данные для первой реализации; ввод добавляй по договору проекта.
        String[] ids = {"iron", "wood"};
        String[] names = {"Железо", "Доски"};
        int[] stocks = {5, 2};

        // TODO: твой сценарий и проверки. Готового решения здесь нет.
        // План: ____________________
        // Критерий: После REGISTER iron=5, wood=2 и TAKE iron:3 lowStock(2) -> [iron,wood].
        // Критерий: TAKE wood:3 отвергнут: wood=2, история не выросла.
        // Критерий: Повтор REGISTER iron отвергнут, исходная запись не заменена.
        // Критерий: INCREASE на Integer.MAX_VALUE при ненулевом остатке отвергнут без
        // переполнения.
    }

    // TODO: твои модели, интерфейсы и методы.
}

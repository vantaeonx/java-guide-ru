package ru.vantaeonx.javaguide.projects;


// Автор: ____________________
// Project06. Симулятор исследовательского рюкзака
public class Project06 {
    // Создай enum Kind { TOOL, MATERIAL, FOOD } и immutable record ItemType(String id,Kind
    // kind,int unitWeight), где id соответствует [a-z][a-z0-9_]{0,15}, unitWeight>0.
    // Backpack имеет maxWeight>0 и LinkedHashMap<ItemType,Integer> количества,
    // неотрицательные int; общий вес long не превышает maxWeight. Add/take проверяют n>0,
    // остаток и переполнение до изменения; нулевой остаток удаляет запись. Repository<T>
    // задаёт save(T) и load(), файловая реализация хранит снимок. Команды: add id n, take
    // id n, list, save, load, exit. Успех изменения -> OK; отказ -> ERROR:причина; list
    // печатает id:count в порядке появления и WEIGHT:число. Save/load в UTF-8 только
    // build/sandbox/project06/backpack.txt: id;count, id берётся из фиксированного
    // каталога. Load сначала проверяет весь снимок, затем заменяет рюкзак целиком; при
    // любой ошибке старое состояние остаётся. Повтор id в снимке запрещён. Формат команды
    // неизвестен -> UNKNOWN, EOF завершает. Exit -> BYE. Конкретный Minecraft API не
    // подключай. В снимке разрешены только положительные count. Методы файлового
    // Repository могут объявлять IOException; граница команды обрабатывает её как ERROR:IO
    // без изменения модели. Во время load отрицательные и нулевые count отвергаются.

    public static void main(String[] args) {
        // Данные для первой реализации; ввод добавляй по договору проекта.
        String[] ids = {"pickaxe", "stone", "apple"};
        String[] kinds = {"TOOL", "MATERIAL", "FOOD"};
        int[] weights = {5, 2, 1};
        long maxWeight = 15;

        // TODO: твой сценарий и проверки. Готового решения здесь нет.
        // План: ____________________
        // Критерий: После add stone 4, add apple 3: stone:4, apple:3, WEIGHT:11.
        // Критерий: Добавление pickaxe 1 отвергнуто, вес остаётся 11; take неизвестного id
        // отвергнут.
        // Критерий: После save, take stone 2, load восстановлены stone:4, apple:3 и вес 11.
        // Критерий: Повреждённый файл, неизвестный id, отрицательное количество, повтор id или
        // превышение веса не меняют текущее состояние.
        // Критерий: Тесты модели запускаются без терминала и файла; Repository<T> не raw type;
        // два рюкзака независимы.
    }

    // TODO: твои модели, интерфейсы и методы.
}

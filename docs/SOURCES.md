# Источники и как ими пользоваться

Материалы написаны на русском для самостоятельного обучения. Определения и особенности
языка сверяются с Java 17, а инструменты — с актуальной официальной документацией.
Дата редакторской сверки: 16 октября 2026 года. Версии интерфейса IDEA могут отличаться.

- [Java Language Specification 17](https://docs.oracle.com/javase/specs/jls/se17/html/index.html):
  формальный договор языка. Главы 4–5 — типы и преобразования, 6–8 — имена и классы,
  9 — интерфейсы, 10 — массивы, 11 — исключения, 14–15 — инструкции и выражения.
- [Java 17 API](https://docs.oracle.com/en/java/javase/17/docs/api/index.html):
  контракт стандартных классов, а не только примеры их использования.
- [String](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html):
  неизменяемость, UTF-16, индексы и split.
- [Scanner](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Scanner.html):
  токены, строки и локаль.
- [List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html):
  дубликаты, порядок и ограничения неизменяемых фабрик.
- [Map](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.html):
  ключи, операции и контракт равенства.
- [Object](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html):
  договор equals и hashCode.
- [Files](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/file/Files.html):
  файловые операции, кодировки, режимы и исключения.
- [javac JDK 25](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html):
  --release, -d, classpath и целевая версия.
- [Первое Java-приложение в IntelliJ IDEA](https://www.jetbrains.com/help/idea/creating-and-running-your-first-java-application.html):
  настройка SDK, проект и запуск main.
- [Maven Compiler Plugin](https://maven.apache.org/plugins/maven-compiler-plugin/):
  конфигурация release и сборка Maven.
- [Python-гайд пользователя](https://github.com/vantaeonx/python-guide-ru):
  педагогическая структура, а не источник Java-кода и готовых ответов.

Если краткая формулировка книги и точный контракт API кажутся несовместимыми,
проверь версию Java, контекст и полный договор метода. Сообщай о дефекте с номером
главы/упражнения и минимальным воспроизводимым примером.
